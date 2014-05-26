#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 12/02/2014

@author: ggomez
'''

import sys
sys.path +=['..']
import libgwnBlocks.gwnBlock as gwn

class EventConsumer(gwn.gwnBlock) :
    '''
    
    '''

    def __init__(self,nickname):
        '''  
        Constructor.
        
        '''
        super(EventConsumer,self).__init__(1,0)
        self.finished = False    
        self.nickname = nickname

        
    def run(self):
		while not self.finished :
			event = self.ports_in[0].get()
			print "Consumer ", self.nickname, "receive event: ", event

    def stop(self):
        self.finished = True
        self._Thread__stop()

