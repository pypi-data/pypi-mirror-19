# -*- encoding: utf-8 -*-
##############################################################################
#
#    Acrisel LTD
#    Copyright (C) 2008- Acrisel (acrisel.com) . All Rights Reserved
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from acris.singleton import NamedSingleton
from acris.sequence import Sequence
from acris.data_types import MergedChainedDict
from acris.threaded import Threaded
import threading
from abc import abstractmethod
from collections import OrderedDict
import queue
from acris.decorated_class import traced_method
import time
import logging
import inspect
from collections import namedtuple

logger=logging.getLogger(__name__)

traced=traced_method(logger.debug, True)

class ResourcePoolError(Exception): pass
class RequestNotFound(Exception): pass

resource_id_sequence=Sequence('Resource_id')

class Resource(object):  

    def __init__(self, *args, **kwargs):
        '''Instantiate Resource to used in Resource Pool
        
        Args:
            name: resource name
        '''
        self.args=args
        self.kwargs=kwargs
        self.id_=resource_id_sequence()
        self.resource_name=self.__class__.__name__
        self.pool=None
        
    def setattrib(self, name, value):
        setattr(self, name, value)
        return self
        
    def __repr__(self):
        result="Resource(name:%s/%s)" % (self.resource_name, self.id_)
        return result 
    
    @abstractmethod
    def activate(self):
        ''' activates resource
        
        Returns:
            activated resource
        '''
        return self
    
    @abstractmethod
    def deactivate(self):
        ''' deactivates resource
        
        Returns:
            deactivated resource
        '''
        return self
        
    @abstractmethod
    def active(self):
        ''' test if resource is active
        '''
        return True
    
Ticket=namedtuple('Ticket', ['pool_name', 'sequence'])

class ResourcePool(NamedSingleton): 
    ''' Singleton pool to managing resources of multiple types.
    
    ResourcePool uses Singleton characteristics to maintain pool per resource name.
    
    Pool policy:
        If there is resource in the pool: provide
        If there is no resource in the pool:
            if limitless, manufacture new by provided resourceFactory
            if limited:
                if nowait: return empty
                if wait with no time limit: wait until resource is available.
                if wait with time limit: halt wait and return with resource if available or empty
                if callback, reserve resource and notify availability with reference to reserved resource
                
    Policy can only be set one immediately after initialization.
    
    '''
    
    __policy = {'autoload': True, # automatically load resources when fall behind
                'load_size': 1, # when autoload, number of resources to load
                'resource_limit': -1, # max resources available
                'activate_on_load': False, # when loading, if set, activate resource
                'activate_on_get': False, # when get, activate resource if not already active
                'deactivate_on_put': False, # when returning resource, deactivate, if set.
        }
    
    __allow_set_policy=True
    __resource_pool_lock=threading.Lock()
    
    __name=''
    
    __ticket_sequence=Sequence('ResourcePool_ticket')
    __pool_id_sequence=Sequence('ResourcePool_pool_id')
    
    def __init__(self, name='', resource_cls=Resource, policy={}):
        # sets resource pool policy overriding defaults
        self.name=name
        self.__resource_cls=resource_cls
        self.__available_resources=dict()
        self.__awaiting=OrderedDict()
        self.__reserved=OrderedDict()
        self.__inuse_resources=dict()
        self.__id=self.__pool_id_sequence()
        #self.mutex = threading.RLock()
        #self.__ticket_sequence=Sequence("ResourcePool.%s" % (resource_cls.__name__, ))
        
        if self.__allow_set_policy:
            self.__policy=MergedChainedDict(policy, self.__policy)
        else:
            #self.__lock.release()
            raise ResourcePoolError("ResourcePool already in use, cannot set_policy")
        
    def __repr__(self):
        return "ResourcePool( class: %s, policy: %s)" % (self.__resource_cls.__name__, self.__policy)
    
    def __sync_acquire(self):
        (frame, filename, line_number,
         function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]
        logger.debug("ResourcePool Acquiring Lock; %s.%s(%s)" % (filename, function_name, line_number))
        self.__resource_pool_lock.acquire()
        
    def __sync_release(self):
        (frame, filename, line_number,
         function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]
        logger.debug("ResourcePool Releasing Lock; %s.%s(%s)" % (filename, function_name, line_number))
        self.__resource_pool_lock.release()
        
    def __load(self, sync=False, count=-1):
        ''' loads resources into pool
        '''
        if sync: self.__sync_acquire()
        self.__allow_set_policy=False
        if count is None or count < 0:
            load_size=self.__policy['load_size']
            resource_limit=self.__policy['resource_limit']
            count=min(load_size, resource_limit) if resource_limit >=0 else load_size
        
        count=count-len(self.__available_resources) 
        if count > 0: 
            activate_on_load=self.__policy['activate_on_load']
            for _ in range(count):
                resource=self.__resource_cls()
                try:
                    if activate_on_load: resource.activate()
                except Exception as e:
                    raise e
                resource.pool=self.name
                
                self.__available_resources[resource.id_]=resource 
        if sync: self.__sync_release()          
    
    def load(self, count=-1):
        ''' loads resources into pool
        '''
        self.__load(sync=True, count=-1)         
        return self
    
    def __remove_ticket(self, ticket, sync=False):
        if sync: self.__sync_acquire()
        logger.debug("Removing reservation ticket: %s, %s" % (ticket, repr(self.__reserved)))
        del self.__reserved[ticket]
        if sync: self.__sync_release()
    
    @Threaded()
    def __wait_on_condition_callback(self, condition, seconds, ticket, callback):
        try:
            with condition:
                condition.wait(seconds)
        except RuntimeError:
            pass
        except Exception as e:
            raise e   
        logger.debug("%s woke up from condition wait: ticket: %s:" % (self.name,ticket,))     
        callback(ticket)
        
    def __wait_on_condition_here(self, condition, seconds, ticket):
        try:
            with condition:
                condition.wait(seconds)
        except RuntimeError:
            pass
        except Exception as e:
            raise e
        
        # process finished waiting either due to time passed
        # or that resources were reserved.  
        # Hence, try to pick reserved resources
        result=self.__reserved.get(ticket, None)
        if result: 
            self.__remove_ticket(ticket)

        return result
            
    def __wait(self, sync, count, wait, callback=None):
        ''' waits for count resources, 
        
        wait uses condition object.  put method would use 
        the same condition object to notify wait of resources 
        reserved for this request.
        
        It is assumed that calling process is separated thread.  
        Otherwise, process deadlocks.
        
        Args:
            sync: (boolean) work in object synchronized, if set
            count: number of resources to wait on
            callback: callable to call back once resources are available
            
        Returns:
            list of resources, if callback is not provided (None)
            reservation ticked to use once called back, if callback is provided.
        
        '''
        seconds=None if wait <0 else wait
        condition = threading.Condition()
        caller=callback.name if hasattr(callback, 'name') else ""
        ticket=Ticket(self.name, self.__ticket_sequence())
        self.__awaiting[ticket]=(condition, count, caller,)
        
        if sync: self.__sync_release()
        
        if not callback:
            result=self.__wait_on_condition_here(condition, seconds, ticket)
        else:
            self.__wait_on_condition_callback(condition, seconds, ticket, callback)
            result=None
         
        return result

    def _get(self, sync=False, count=1, wait=-1, callback=None, hold_time=None, ticket=None):
        self.__allow_set_policy=False
        
        if ticket is not None:
            # process finished waiting either due to time passed
            # or that resources were reserved.  
            # Hence, try to pick reserved resources
            logger.debug("%s Addressing get with ticket %s" % (self.name, ticket))
            result=self.__reserved.get(ticket, None)
            if result: 
                logger.debug("%s found ticket %s" % (self.name, ticket))
                self.__remove_ticket(ticket=ticket, sync=sync)
                return result
            else:
                logger.debug("%s ticket %s not fond" % (self.name, ticket))
                     
        resource_limit=self.__policy['resource_limit']
        if resource_limit > -1 and count >resource_limit:
            raise ResourcePoolError("Trying to get count (%s) larger than resource limit (%s)" % (count, resource_limit))
        
        if sync: self.__sync_acquire()
        
        activate_on_get=self.__policy['activate_on_get']
        # If there are awaiting processes, wait too, and this call is not after
        # put (for an awated process).
        if len(self.__awaiting) > 0 and sync:
            resources=self.__wait(sync=sync, count=count, wait=wait, callback=callback)
            if activate_on_get: self.__activate_allocated_resource(resources)
            return resources
        
        # try to see if request can be addressed by existing or by loading new 
        # resources.
        available_loaded=len(self.__available_resources)
        inuse_resources=len(self.__inuse_resources)
        hot_resources=available_loaded+inuse_resources
        missing_to_serve=count-available_loaded
        if missing_to_serve < 0: missing_to_serve=0
        allowed_to_load=resource_limit-hot_resources if resource_limit > 0 else missing_to_serve
        
        to_load=min(missing_to_serve, allowed_to_load)
        
        #print("TOLOAD: %s (available_loaded: %s, missing_to_serve: %s, allowed_to_load: %s, inuse_resources %s, hot_resources: %s)" % \
        #      (to_load, available_loaded, missing_to_serve, allowed_to_load, inuse_resources, hot_resources))
        if to_load > 0:
            self.__load(sync=False, count=to_load)
            
        # if resources are available to serve the request, do so.
        # if not, and there is wait, then do wait.
        # otherwise return no resources.
        if len(self.__available_resources) >= count:
            # There are enough resources to serve!
            resource_names=list(self.__available_resources.keys())[:count]
            resources=list()
            logger.debug('%s assigning %s to inuse' % (self.name, resource_names,))
            for name in resource_names:
                resource=self.__available_resources[name]
                resources.append(resource)
                del self.__available_resources[name]
                self.__inuse_resources[name]=resource
            if sync: self.__sync_release()
        elif wait != 0:
            # No resources.  But need to wait.
            resources=self.__wait(sync=sync, count=count, wait=wait, callback=callback)
        else:
            # No resources and no need to wait; we are done!
            resources=[]
            if sync: self.__sync_release()
            pass
        
        if activate_on_get: self.__activate_allocated_resource(resources)
        return resources
    
    def get(self, count=1, wait=-1, callback=None, hold_time=None, expire=None, ticket=None):
        ''' retrieve resource from pool
        
        get checks for availability of count resources. If available: provide.
        If not available, and no wait, return empty
        If wait, wait for a seconds.  If wait < 0, wait until available.
        If about to return empty and callback is provided, register reserved with hold_time.
        When reserved, callback will be initiated with reservation_ticket.  The receiver, must call
        get(reservation_ticket=reservation_ticket) again to collect reserved resources.
        
        Important, when using wait, it is assumed that calling process is separated thread.  
        Otherwise, process deadlocks.

        Warnings: 
            1. if count > resource_limit, call will be rejected.  
            2. if count > 1 and resources are limited due to high activity or 
                clients not putting back resources, caller may be in deadlock.
            
        Args:
            count: number of resource to grab 
            wait: number of seconds to wait if none available. 
                0: don't wait
                negative: wait until available
                positive: wait period
            callback: notify that resources are available to collect
            hold_time: seconds to hold reserve resources on callback.  
                If not collected in within the specify period, reserved go
                back to pull.
            expire: seconds to limit use of resources
            ticket: reserved ticket provided in callback to allow client pick their 
                reserved resources. 
            
        Raises:
            ResourcePoolError
        '''
        
        # some validation:
        if callback and not callable(callback):
            raise ResourcePoolError("Callback must be callable, but it is no: %s" % repr(callback))
        
        result=self._get(sync=True, count=count, wait=wait, callback=callback, hold_time=hold_time, ticket=ticket)
        return result

    
    def __activate_allocated_resource(self, resources):
        for resource in resources:
            try:
                if not resource.active: resource.activate()
            except Exception as e:
                raise e
                   
    def put(self, *resources):
        ''' adds resource to this pool
        
        Args:
            resource: Resource object to be added to pool
        '''
        
        # validate that all resources provided are legal
        self.__sync_acquire()
        pool_resource_name=self.__resource_cls.__name__
        
        for resource in resources: 
            resource_name=resource.__class__.__name__
            if pool_resource_name != resource_name:
                raise ResourcePoolError("ResourcePool resource class (%s) doesn't match returned resource (%s)" % \
                                        (pool_resource_name, resource_name))
            if resource.id_ in self.__available_resources.keys():
                raise ResourcePoolError("Resource (%s) already in pool's available (%s)" % \
                                        (resource_name, pool_resource_name, ))                
            if resource.id_ not in self.__inuse_resources.keys():
                raise ResourcePoolError("Resource (%s) not in pool's inuse (%s)" % \
                                        (resource_name, pool_resource_name, ))
                
        # deposit resource back to available
        resources=list(resources)
        deactivate_on_put=self.__policy['deactivate_on_put']
                
        for resource in resources: 
            if deactivate_on_put: 
                try:
                    resource.deactivate()
                except Exception as e:
                    self.__sync_release()
                    raise e
            self.__available_resources[resource.id_]=resource
            del self.__inuse_resources[resource.id_]
            logger.debug("%s adding to available, removing from inuse %s (available: %s, inuse: %s)" % (self.name, resource, len(self.__available_resources), len(self.__inuse_resources)))
        
        
        for ticket, (condition, count, caller) in list(self.__awaiting.items()):
            logger.debug("%s, %s found %s awaiting; require: %s, available: %s:" % (caller, self.name, ticket, count, len(self.__available_resources)))
            if count <= len(self.__available_resources):
                self.__reserved[ticket]=self._get(count=count)
                with condition:
                    logger.debug("%s, %s notifying: %s:" % (caller, self.name, ticket,))
                    condition.notify()
                del self.__awaiting[ticket]
            else:
                # this is an interesting scenario.
                # e.g., first awaiting for 3 resources. But there is only one available.
                #       second awaits for 1 resources.  If we serve it, first will have 
                #       to wait longer.  If we don't, first is holding the line.
                #       Predictive module will learn if it is better to hold the line,
                #       
                break
        self.__sync_release()      


class RequestorCallback(object):
    def __init__(self, notify_queue):
        self.q=notify_queue
    def __call__(self, ticket=None):
        logger.debug('RequestorCallback notifying ticket: %s' %(ticket,))
        self.q.put(ticket)

class Requestor(object):
    ''' Manages a single request from multiple resource pools
    '''
        
    def __init__(self, request, wait=-1, callback=None, hold_time=None, expire=None, audit=True):
        '''Initialize requestor object to manage request from multiple pools
        
        Args:
            request: iterator on tuples of resource pool object and quantity of resources required
            wait: seconds to wait for resources
            callback: callable to callback when resources are reserved
            hold_time: how long to hold resources in reserved
            expire: seconds to limit use of resources.
            audit: if True, ensures resources returened are from the same requestor 
            
        '''
        self.__request=dict([(r.name, (r,count)) for r, count in request])
        self.__wait=wait
        self.__callback=callback
        self.__hold_time=hold_time
        self.__notify_queue=queue.Queue()
        self.__tickets=list()
        self.__resources=dict()
        self.__reserved=False
        self.__resource_pool_requestor_lock=threading.Lock()
        self.__collect_resources_started=False
        self.__audit=audit
        if callback and hasattr(callback, 'name'):
            self.__client_name=callback.name
        else: self.__client_name=''
        self.__get()
    
    def __sync_acquire(self):
        (frame, filename, line_number,
         function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]
        logger.debug("ResourcePoolRequestor Acquiring Lock; %s.%s(%s)" % (filename, function_name, line_number))
        self.__resource_pool_requestor_lock.acquire()
        
    def __sync_release(self):
        (frame, filename, line_number,
         function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]
        logger.debug("ResourcePoolRequestor Releasing Lock; %s.%s(%s)" % (filename, function_name, line_number))
        self.__resource_pool_requestor_lock.release()

    def __is_reserved(self):
        ''' Returns True if all resources are collected
        '''
        missings=set(self.__request.keys()) - set(self.__resources.keys())
        self.__reserved=len(missings) ==0
        #if not self.__reserved:
        #    logger.debug("%s missing resources %s" %(self.__client_name, missings))
        return self.__reserved
        
    def is_reserved(self):
        ''' Returns True if all resources are collected
        '''
        return self.__reserved
        
    def __get(self):
        callback=RequestorCallback(self.__notify_queue) if self.__callback else None
        for rp, count in self.__request.values():
            logger.debug("%s requesting resources %s(%s)" %(self.__client_name, rp.name, count))
            response=rp.get(count=count, wait=self.__wait, callback=callback, hold_time=self.__hold_time)
            
            if response:
                logger.debug("%s received resources %s" %(self.__client_name, response))
                self.__resources[rp.name]=dict([(r.id_, r) for r in response])
                
        if not self.__is_reserved():
            go_collect=False
            self.__sync_acquire()
            if not self.__collect_resources_started:
                go_collect=True
                self.__collect_resources_started=True
            self.__sync_release()
            if go_collect:
                logger.debug("%s going to collect missing resources" % (self.__client_name, ))
                self.__collect_resources()   
        else:
            self.__notify_collected()
    
    @Threaded()
    def __collect_resources(self):
        start_time=time.time()
        go=True
        wait=self.__wait if self.__wait is None or self.__wait >=0 else None
        while go:
            logger.debug("%s trying to get from notify queue (wait: %s)" %(self.__client_name, wait))
            try:
                ticket=self.__notify_queue.get(timeout=wait)
            except queue.Empty:
                ticket=(None, None)
            rp_name=ticket.pool_name
            
            if ticket:
                rp, _=self.__request[rp_name]
                resources=rp.get(ticket=ticket)
                logger.debug("Collected resources %s" %(resources))
                self.__resources[rp_name]=dict([(r.id_, r) for r in resources])
                
            time_passed=time.time() - start_time
            if self.__wait and self.__wait >0:
                wait=self.__wait - time_passed
                go=wait > 0
            logger.debug("%s all reserved %s" % (self.__client_name, self.__is_reserved(),))
            go=go and not self.__is_reserved()
        
        if not self.__is_reserved():
            for rp_name, resources in list(self.__resources.items()):
                rp, _=self.__request[rp_name]
                returning=list(resources.values())
                rp.put(*returning)
                del self.__resources[rp_name]               
        else:
            self.__notify_collected()
                 
    def __notify_collected(self):
        if self.__is_reserved() and self.__callback:
            self.__callback(True)
                  
    def get(self,):
        result=None
        if self.__is_reserved():
            result=list()
            for k, r in list(self.__resources.items()): 
                result.extend(r.values()) 
                if not self.__audit: del self.__resources[k]
             
        return result 
            
    def put(self, *resources):
        logger.debug("%s putting back resources %s" % (self.__client_name, repr(resources)))
        
        # ensure resources returned are in alignment with this container.
        #resource_to_return=list()
        for resource in resources:
            rp_name=resource.pool 
            failed=False 
            try:
                rp, _ = self.__request[rp_name]
            except KeyError:
                failed=True
                logger.error("%s ResourcePool %s not found; cannot return resource %s" % (self.__client_name, rp_name, resource))
            else:
                # There are two cases; if audited, and if not
                # When audited, returning resource only if part of this request.
                # If not audited, return anyway.
                found=True
                if len(self.__resources) >0:
                    rp_resources=self.__resources[rp_name]
                    try:
                        del rp_resources[resource.id_]
                    except:
                        found=False
                        logger.error("%s resource %s not found in pool %s; cannot return." % (self.__client_name, resource, rp_name))
                if found:
                    #resource_to_return.append(resource)
                    logger.debug("%s returning %s to pool %s" % (self.__client_name, repr(resource), rp.name))
                    rp.put(resource)
                failed=failed or not found
                
        if failed:
            raise ResourcePoolError("%s failed to return resources." % (self.__client_name, ))
        
    def __del__(self):
        # need to make sure all resources are returned
        for rp_name, resources in self.__resources.items():
            rp, _ = self.__request[rp_name]
            for resource in resources.values():
                rp.put(resource)
                
        # TODO: notify ResourcePool that not waiting on resources anymore.


class RequestorsCallback(object):
    def __init__(self, notify_queue, request_id):
        self.q=notify_queue
        self.request_id=request_id
    def __call__(self, ticket=None):
        logger.debug('RequestorsCallback notifying request id %s ticket: %s' % (self.request_id, ticket, ))
        self.q.put( (ticket, self.request_id,) )
         
#Pool=namedtuple('Pool', ['pool', 'reserved', 'inuse'])

class Requestors(object):
    ''' Manages multiple requests from multiple resource pools
    '''
    
    __request_id=Sequence("Requestors_request_id")
    
    class Request(object):
        def __init__(self, request_id, request, wait=-1, callback=None, hold_time=None, expire=None):
            self.request_id=request_id
            self.request=dict([(r.name, (r,count)) for r, count in request])
            self.wait=wait
            self.callback=callback
            self.hold_time=hold_time
            self.reserved=False
            self.fetched=False
            self.resources=dict()
            self.start_time=time.time()
            if callback and hasattr(callback, 'name'):
                self.client_name=callback.name
            else: self.client_name=''
            
        def __repr__(self):
            return "%s" %(self.request_id, )
        
    def __init__(self, audit=False):
        self.__audit=audit
        self.__pools=dict() # mapping for pool names to namedtuple of pool, requestor, and resources
        self.__requests=dict()
        self.__notify_queue=queue.Queue()
        self.__resource_pool_requestor_lock=threading.Lock()
        self.__collect_resources_started=False
        
    def reserve(self, request, wait=-1, callback=None, hold_time=None, expire=None,):
        '''Initialize requestor object to manage request from multiple pools
        
        Args:
            request: iterator on tuples of resource pool object and quantity of resources required
            wait: seconds to wait for resources
            callback: callable to callback when resources are reserved
            hold_time: how long to hold resources in reserved
            expire: seconds to limit use of resources.
            audit: if True, ensures resources returned are from the same requestor 
            
        '''
        request_id=self.__request_id()
        self.__requests[request_id]=self.Request(request_id=request_id, request=request, wait=wait, callback=callback, hold_time=hold_time, expire=expire)        
        self.__get(request_id)
        return request_id
    
    def __sync_acquire(self):
        (frame, filename, line_number,
         function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]
        logger.debug("ResourcePoolRequestors Acquiring Lock; %s.%s(%s)" % (filename, function_name, line_number))
        self.__resource_pool_requestor_lock.acquire()
        
    def __sync_release(self):
        (frame, filename, line_number,
         function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]
        logger.debug("ResourcePoolRequestors Releasing Lock; %s.%s(%s)" % (filename, function_name, line_number))
        self.__resource_pool_requestor_lock.release()

    def __is_reserved(self, request_id):
        ''' Returns True if all resources are collected
        '''
        request=self.__get_request(request_id)
        
        missings=set(request.request.keys()) - set(request.resources.keys())
        request.reserved=len(missings) ==0
        if not request.reserved:
            logger.debug("%s missing resources %s" %(request.client_name, missings))
        return request.reserved
        
    def is_reserved(self, request_id):
        ''' Returns True if all resources are collected
        '''
        try:
            result=self.__requests[request_id].reserved
        except:
            raise ResourcePoolError("Unknown request_id: %s" % request_id)
        return result
        
    def __get(self, request_id):
        request=self.__get_request(request_id)
        callback=RequestorsCallback(self.__notify_queue, request_id=request_id) if request.callback else None
        for rp, count in request.request.values():
            logger.debug("%s requesting resources %s(%s)" %(request.client_name, rp.name, count))
            resources=rp.get(count=count, wait=request.wait, callback=callback, hold_time=request.hold_time)
            
            if resources:
                logger.debug("%s received resources %s" %(request.client_name, resources))
                #self.__sync_acquire()
                self.__update_resource_store(request_id=request_id, resource_pool=rp, resources=resources)
                #self.__sync_release()
                
        if not self.__is_reserved(request_id):
            go_collect=False
            #self.__sync_acquire()
            logger.debug("%s __collect_resources_started %s" %(request.client_name, self.__collect_resources_started))
            if not self.__collect_resources_started:
                go_collect=True
                self.__collect_resources_started=True
            #self.__sync_release()
            if go_collect:
                logger.debug("%s starting collector" % (request.client_name, ))
                self.__collect_resources()   
        else:
            self.__sync_acquire()
            self.__notify_collected(request_id)
            self.__sync_release()
            
    def __return_resources(self, request_id):
        logger.debug("returning resources  for request id: %s" %(request_id,))
        request=self.__get_request(request_id)
        for rp_name, resources in list(request.resources.items()):
            rp=self.__pools[rp_name]
            returning=list(resources.values())
            rp.put(*returning)
            del request.resources[rp_name]               
    
    def __update_resource_store(self, request_id, resource_pool, resources):
        logger.debug("Collected resources %s" %(resources))
        request=self.__get_request(request_id)
        
        request.resources[resource_pool.name]=dict([(r.id_, r.setattrib('requestor_request_id', request_id)) for r in resources])
        # plasce resources in reserved
        self.__pools[resource_pool.name]=resource_pool
        '''
        try:
            pool=self.__pools[resource_pool.name]
        except KeyError:
            pool=Pool(resource_pool, dict(), dict())
            self.__pools[resource_pool.name]=pool
        pool.reserved.update(request.resources[resource_pool.name])
        #rp_resources.extend(map(lambda x: x.setattrib('__requestors_request_id', request_id), resources))
        '''
        return self.__is_reserved(request_id)
    
    def __get_request(self, request_id, default=None):
        request=self.__requests.get(request_id, None)
        if request is None and default is None:
            (frame, filename, line_number,
             function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]            
            raise RequestNotFound("Unknown request_id: %s: %s(%s)" % (request_id, function_name, line_number,))
        elif request is None:
            request=default
        return request
    
    def __evaluate_collect_wait_time(self):
        waits=list() 
        found_endless_waiter=False 
        for request_id, request in self.__requests.items():
            if self.__is_reserved(request_id): continue
            time_passed=time.time() - request.start_time
            if request.wait and request.wait >0:
                wait=request.wait - time_passed
                if wait<= 0: 
                    self.__return_resources(request_id)
                else: waits.append(wait)
            else:
                found_endless_waiter=True
        self.__collect_resources_started=len(waits)>0 or found_endless_waiter
        len_waits=len(waits)
        wait=min(waits) if len_waits>0 else None  
        logger.debug("Wait evaluated: %s: waits: %s: found endless: %s" %(wait, len(waits), found_endless_waiter,))
        return wait
    
    @Threaded()
    def __collect_resources(self):
        wait=self.__evaluate_collect_wait_time()
        logger.debug("starting get loop (wait: %s, collect: %s)" %(wait,self.__collect_resources_started))
        #self.__collect_resources_started=True
        while self.__collect_resources_started:
            logger.debug("trying to get from notify queue (wait: %s)" %(wait,))
            try:
                ticket, request_id=self.__notify_queue.get(timeout=wait)
            except queue.Empty:
                ticket, request_id=None, None
            
            logger.debug("got something from notify queue request_id: %s, ticket: %s" %(request_id, ticket,))
            
            self.__sync_acquire()
            
            if request_id is not None:
                rp_name=ticket.pool_name
                request=self.__get_request(request_id)
                logger.debug("%s received resources for request_id %s" %(request.client_name, request_id,))
                rp, _=request.request[rp_name]
                resources=rp.get(ticket=ticket)
                reserved=self.__update_resource_store(request_id=request_id, resource_pool=rp, resources=resources)
                if reserved:
                    self.__notify_collected(request_id)          
            
            wait=self.__evaluate_collect_wait_time()
            
            self.__sync_release()
                    
    def __notify_collected(self, request_id):
        request=self.__get_request(request_id)
        if self.__is_reserved(request_id) and request.callback:
            logger.debug("%s Calling callback for %s" %(request.client_name, request_id,))
            request.callback(request_id)
                  
    def was_fetched(self, request_id):
        request=self.__get_request(request_id)
        return request.fetched
    
    def get(self, request_id):
        result=None
        request=self.__get_request(request_id)
        self.__sync_acquire()
        if request.reserved and not request.fetched:
            result=list()
            for _, resources in list(request.resources.items()): 
                result.extend(resources.values()) 
            request.request.clear()
            request.fetched=True
            logger.debug("%s remove required and resources %s" %(request.client_name, request_id,))
        self.__sync_release() 
        
        return result 
            
    def put(self, *resources):
        self.__sync_acquire()
        logger.debug("putting back resources %s" % (repr(resources)))
        
        # ensure resources returned are in alignment with this container.
        #resource_to_return=list()
        for resource in resources:            
            rp_name=resource.pool 
            failed=False 
            try:
                rp= self.__pools[rp_name]
            except KeyError:
                failed=True
                logger.error("ResourcePool %s not found; cannot return resource %s" % (rp_name, resource))
            else:
                # There are two cases; if audited, and if not
                # When audited, returning resource only if part of this request.
                # If not audited, return anyway.
                #rp=pool.pool
                logger.debug("Returning %s to pool %s" % (repr(resource), rp.name))
                rp.put(resource)
                request_id=resource.requestor_request_id
                request=self.__requests[request_id]
                del request.resources[rp_name][resource.id_]
                #del pool.inuse[resource.id_]
                
        if failed:
            raise ResourcePoolError("Failed to return resources." )
        self.__sync_release()

    def put_requested(self, request_id):
        ''' returns fetched request formated as in get.
        
        Args:
            request: list of tuples of resource pool and amount requested
        '''
        self.__sync_acquire()
        logger.debug("putting back request id: %s" % (repr(request_id)))
        
        # ensure resources returned are in alignment with this container.
        #resource_to_return=list()
        request=self.__requests[request_id]
        for rp_name, resources in request.resources.items():
            failed=False 
            try:
                rp= self.__pools[rp_name]
            except KeyError:
                failed=True
                logger.error("ResourcePool %s not found; cannot return resources" % (rp_name, ))
            else:
                # There are two cases; if audited, and if not
                # When audited, returning resource only if part of this request.
                # If not audited, return anyway.
                #logger.debug("Returning %s to pool %s" % (repr(resource), rp.name))
                for resource in resources:
                    rp.put(resource)
            
            
        if failed:
            raise ResourcePoolError("Failed to return resources." )
        self.__sync_release()
        
    # TODO: rebuild del of captured resources
    def __del__(self):
    #    # need to make sure all resources are returned
        for request_id, request in self.__requests.items():
            for rp_name, resources in request.resources.items():
                rp=self.__pools[rp_name]
                for resource in resources.values():
                    rp.put(resource)

