#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# schedEvToFr.py
#



import sys
#sys.path +=['..']

import gwnevents.if_events as if_events
import gwnblocks.gwnblock as gwn



class Framer(gwn.GWNBlock):
    '''An Framer based on IEEE 802.11 frames.

    Gets an event from the Events input queue, generates the corresponding frame, puts it into the Event, and puts the event in the output queue.
    '''

    def __init__(self):
        '''Constructor.
        '''
        super(Framer, self).__init__(1, 'Framer', 1, 1)        
        self.finished= False


    def process_data(self, port_type, port_nr, ev):
        '''Generates a frame and includes it into an ouput event.
        
        From the event received, generates a frame, assigns the frame as an atrribute in the same event, and outputs the event.
        '''
        frmobj = if_events.evtofrm(ev)
        framepkt = frmobj.mkpkt()
        ev.frmpkt = framepkt
        self.write_out(0, ev)
        return



if __name__ == '__main__':
    import doctest
    testfilename = sys.argv[0][:-2] + 'txt'
    try:
        doctest.testfile(testfilename)
    except:      # no text file present
        pass

