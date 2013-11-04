#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# sched-bytype.py
#


'''A scheduler that gets a events from Layer 3 input queue, generates the corresponding event, and puts it into the Layer 2 queue .
   We now asume that the events generated by L3 are the same of L2, so this schedule for the moment is only a gateway that takes the
   events form the input queue and put the same events in the output queue
'''
import Queue
import sys
sys.path +=['..']
import libevents.if_events as events
# The next import is defined only for test
import libevents.events as Events

import libutils.gnscheduler as Scheduler


class SchedLayer3(Scheduler.Scheduler):
    '''Subclass of Scheduler for adapting layers 3 and 2.
    '''

    def fn_sched(self):
        '''Scheduling function, reads events, outputs events.
        
        Reads one element from the input event queue, and puts the event in the output queue.
        out_queues: a dictionary of {nm_queue: (out_queue)}; nm_queue is a name for the queue, out_queue is the output queue.
        '''
        in_qu = self.in_queues[0]
        event = in_qu.get(True)
        out_queue = self.out_queues['event']
        out_queue.put(event, False)   # add to queue, don't block         
        in_qu.task_done()
        return



def test():
    '''Tests on events.

    Events are put in output queue.
    '''

    # create input queue
    layer3_q = Queue.Queue(10)
    layer2_q = Queue.Queue(10)
    out_queues = { \
        'event': (layer2_q)  \
        }
    sch = SchedLayer3(layer3_q, out_queues)

    # put events in input queue
    for i in range(1, 5) :
        ev = Events.mkevent('DataData')
        ev.src_addr = "100"
        ev.dst_addr=  "150"
        print " Event = ", ev
        layer3_q.put(ev,False)
    print 'Input queue size', layer3_q.qsize()

    # create and start scheduler
    print '\n=== Process ==='
    sch.start()
    layer3_q.join()
    sch.stop()
    sch.join()

    print '\n=== Read the output queues ==='
    print 'Queue size:', layer2_q.qsize()
    while not layer2_q.empty():
        item = layer2_q.get()
        print "Event", item
    return
    
    


if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        sys.exit()

