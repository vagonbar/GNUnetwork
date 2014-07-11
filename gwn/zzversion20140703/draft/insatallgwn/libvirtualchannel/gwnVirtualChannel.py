#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Thu Dec 13 14:31:45 2012

@author: belza
'''
import sys,random
sys.path +=sys.path + ['..']
from libutils.gwnscheduler2 import Scheduler

class gwnVirtualChannel(Scheduler):
    '''
    '''

    def __init__(self,frame_loss):
        '''  
        Constructor.
        
        '''        
        super(gwnVirtualChannel,self).__init__(1,1)
        self.frame_loss = frame_loss        
        self.finished = False
        
    def fn_sched(self):
        '''
        '''
        in_qu = self.ports_in[0]
        if in_qu:
            if not in_qu.empty():
                event = in_qu.get()
                a =random.random()
                if a > self.frame_loss:                    
                    for q in self.ports_out[0]:
                        q.put(event,False)                
        else:
            print 'ERROR; No input queue defined'   # shows sometimes...
        return
