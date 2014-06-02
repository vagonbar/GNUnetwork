#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# schedEvToFr.py
#


'''An Framer based on IEEE 802.11 frames.

Gets an event from the Events input queue, generates the corresponding frame, puts it into the Event, and puts the event in the output queue.
'''

import sys
sys.path +=['..']

import libevents.if_events as if_events
import libgwnBlocks.gwnBlock as gwn



class gwnFramer(gwn.gwnBlock):
    '''
    '''
    def __init__(self):
        '''  
        Constructor
        
        '''
        super(gwnFramer,self).__init__(1,1)        
        self.finished= False


    def run(self):
        '''
        
        Reads one element from the input event queue, generates a frame, and puts the event with this frame in  the output queues.
        
        '''
        while not self.finished :
            in_qu = self.ports_in[0]
            event = in_qu.get(True)
            
            frmobj = if_events.evtofrm(event)
            framepkt = frmobj.mkpkt()
            event.frmpkt = framepkt
            for q in self.ports_out[0]:
                q.put(event, False)   # add to queue, don't block  
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

