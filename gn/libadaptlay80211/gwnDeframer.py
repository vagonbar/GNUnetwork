#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# sched-bytype.py
#


'''A frame to event scheduler, based on IEEE 802.11 frames.

A scheduler that gets a frame from a Layer 1 input queue, generates the corresponding event, and puts it into Management, Control or Data queues based on the event type.
'''
import sys
sys.path +=['..']

import libevents.if_events as if_events
import libframes.if_frames as if_frames
import libgwnBlocks.gwnBlock as gwn




class gwnDeframer(gwn.gwnBlock):
    '''
    '''
    def __init__(self):
        '''  
        Constructor
        
        '''
        super(gwnDeframer,self).__init__(1,1)        
        self.finished= False


    def run(self):
        ''' reads frames, outputs events by type.
        
        Scheduler function to process a frames queue: reads one element from the input frame queue, generates an event, and puts the event in one of the output queues according to its type.
        
        '''
        while not self.finished :
            in_qu = self.ports_in[0]
            evframe = in_qu.get(True)
            #print " recibi frame : ", repr(frame)
            frm_obj = if_frames.objfrompkt(evframe.frmpkt)
            event = if_events.frmtoev(frm_obj)
            #print "recibi event : ", event
            if event != None:
                for q in self.ports_out[0]:
                    q.put(event, False)   # add to queue, don't block            
            else:
                    raise if_events.EventFrameException('Scheduler, error in \
                        frame')
            in_qu.task_done()
            

    def stop(self):        
       self.finished = True
       self._Thread__stop()



if __name__ == '__main__':
    import doctest
    testfilename = sys.argv[0][:-2] + 'txt'
    try:
        doctest.testfile(testfilename)
    except:      # no text file present
        pass
