#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    This file is part of GNUWiNetwork,
#    Copyright (C) 2014 by 
#        Pablo Belzarena, Gabriel Gomez Sena, Victor Gonzalez Barbone,
#        Facultad de Ingenieria, Universidad de la Republica, Uruguay.
#
#    GNUWiNetwork is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    GNUWiNetwork is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with GNUWiNetwork.  If not, see <http://www.gnu.org/licenses/>.
#


'''An IEEE 802.11 deframer block.
'''


import sys

import utils.framers.ieee80211.if_frames as if_frames
import gwnevents.if_events as if_events
import gwnblocks.gwnblock as gwn


class Deframer(gwn.GWNBlock):
    '''A frame to event scheduler, based on IEEE 802.11 frames.

    Receives A scheduler that gets a frame from a Layer 1 input queue, generates the corresponding event, and puts it into Management, Control or Data queues based on the event type.
    '''
    def __init__(self):
        '''Constructor
        '''
        super(Deframer,self).__init__(1, 'Deframer', 1, 1)
        self.finished = False


    def process_data(self, port_type, port_nr, ev):
        '''Reads frames, outputs events by type.
        
        Scheduler function to process a frames queue: reads one element from the input frame queue, generates an event, and puts the event in one of the output queues according to its type.
        '''
        frm_obj = if_frames.objfrompkt(ev.frmpkt)
        ev_out = if_events.frmtoev(frm_obj)
        #print "recibi event : ", event
        if ev_out != None:
            self.write_out(0, ev_out)
        else:
            raise if_events.EventFrameException('Deframer, error in frame')


if __name__ == '__main__':
    import doctest
    testfilename = sys.argv[0][:-2] + 'txt'
    try:
        doctest.testfile(testfilename)
    except:      # no text file present
        pass

