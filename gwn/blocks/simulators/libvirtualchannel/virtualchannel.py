#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Thu Dec 13 14:31:45 2012

@author: belza
'''

import sys
import random

sys.path +=sys.path + ['..']
#from libutils.gwnscheduler2 import Scheduler
import libgwnblocks.gwnblock as gwnblock



class GWNVirtualChannel(gwnblock.GWNBlock):
    '''A virtual channel emulating frame loss.
    '''


    def __init__(self,frame_loss):
        ''' Constructor.
        
        @param frame_loss: rate of frame loss, in [0, 1]; 0 is no loss, all frames transferred; 1 is total loss, no frame transferred.
        '''        
        super(GWNVirtualChannel, self).__init__(1, 'VirtualChann1', 1, 1)
        self.frame_loss = frame_loss        
        self.finished = False


    def process_data(self, port_type, port_nr, ev):
        '''Transfers event from input to output with probability of loss.
        '''
        a = random.random()
        if a > self.frame_loss:
            self.write_out(0, ev)
        return


