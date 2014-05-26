#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Thu Dec 13 14:31:45 2012

@author: belza
'''
import sys
sys.path +=sys.path + ['..']
from gwnscheduler2 import Scheduler

class EvtypeClassifier(Scheduler):
    '''A timerthat waits an interval and generates a Timer Event.
    This class is a timer that waits for a given interval. After that generates an event of Yype TIMER and Subtype the name given in subTypeEvent1.
    The timer retries the number of times gven in the parameter retry. After the given number of retries it generates the event of Type TIMER and subtype given in subTypeEvent2 if it is not None.
    '''

    def __init__(self, n_out=1,list_types=[]):
        '''  
        Constructor.
        
        @param interval: The interval of time.
        @param retry: The number of retries.
        @param nickname1: The nickname of the event that must be called after each retry.
        @param nickname2: The nickname of the event that must be called after the given number of retries.
        @param add_info: additional information that will be send with the Timer Event.
        '''        
        "The Timer has one output and 0 inputs so we must call the father constructor with parameters (0,1)"
        super(EvtypeClassifier,self).__init__(1,n_out)        
        self.list_types =list_types
        self.finished = False
        
    def fn_sched(self):
        '''Scheduling function to process queue elements acording to type.
        
        Reads one element from one of the input queues, examines element, acts according to its type, as stated in out_queues.
        out_queues: a dictionary of {nm_queue: (fn_queue, out_queue)}. The item_type is a string; the function returns an element to put in the output queue.
        '''
        in_qu = self.ports_in[0]
        if in_qu:
            if not in_qu.empty():
                event = in_qu.get()
                for item_type in self.list_types:
                    if event.ev_type == item_type:
                    # function to execute, output queue
                        index = self.list_types.index(item_type)
                        for q in self.ports_out[index]:
                            q.put(event,False)                
        else:
            print 'ERROR; No input queue defined'   # shows sometimes...
        return
