#!/usr/bin/env python
# -*- coding: utf-8 -*-

# scheduler: a generic scheduler

'''Classes and Functions to implement a generic scheduler.

How to use:
  1. Create a subclass of Scheduler.
  2. Overwrite fn_sched() in the subclass.
  3. Write a test function to verify behavior.

In class C{Scheduler}, C{in_queues} and C{out_queues} may be any structure understood by C{fn_sched()}. This function C{fn_sched()} must get items from input queues, optionally do some work, and put items in output queues.

Examples of queue structures:
  - C{{name: queue}}, a dictionary of queues identified by name.
  - C{{priority:queue}}, a dictionary of queues by priority, 1<= priority <=10.
  - C{[queue]}, a list of queues, e.g. to put on the shortest, or to get from the longest.
  - C{{name: (function, queue)}}, a dictionary of tuples; name identifies queue, function is a task to perform specific to one queue. The function may even produce a different item to put in queue.
'''

import sys
sys.path +=sys.path + ['..']
import libgwnBlocks.gwnBlock as gwn


class Scheduler(gwn.gwnBlock):
    '''Gets elements from input queues, processes, puts elements in output queues.
    
    This scheduler gets one element from one of several input queues, and puts elements in one or several output queues. Behaviour is regulated by a scheduling function which is expected to be overwritten when subclassing this class. Selection of input queue to get element from, processing, creation of one or more elements of same or different type, and putting elements in output queues are all regulated by this scheduling function.
    '''
 
    def __init__(self,n_in=1,n_out=1,debug=False):
        '''Constructor.
        @param n_in: number of input queues
        @param n_out: numer of output lists of queues
        @param debug: if True prints some debug messages; default False.
        '''
        super(Scheduler,self).__init__(n_in,n_out)       
        if debug:
            print "inicializo"
        self.daemon = True
        self.finished = False

    def fn_sched(self):
        '''A dummy scheduling function; to be overwritten in a subclass.
        '''
        pass
        return


    def run(self, debug=False):
        '''Runs the scheduler until stopped.

        @param debug: if True prints some debug messages; default False.
        '''
        if debug:
            print "start .... run"
        while not self.finished:
            self.fn_sched()
        else:
            #print 'Scheduler, stopped'
            self.stop()


    def stop(self, debug=False):
        '''Stops the scheduler.

        @param debug: if True prints some debug messages; default False.
        '''
        if debug:
            print 'Scheduler, in stop function'
        self.finished = True
        self._Thread__stop()



