#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 12/02/2014

@author: ggomez
'''

import sys
sys.path +=['..']
import libgwnblocks.gwnblock as gwn

class EventConsumer(gwn.GWNBlock) :
    '''
    
    '''

    def __init__(self,nickname):
        '''  
        Constructor.
        
        '''
        super(EventConsumer,self).__init__(1,nickname,1,0)
        self.nickname = nickname

        
    def process_data(self, port_type, port_nr, ev):
        '''This is the private thread that generates.
        '''

        if port_type == "inport":
		print "Consumer ", self.nickname, "receive event: ", ev


