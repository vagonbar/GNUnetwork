#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Thu Dec 13 14:31:45 2012

@author: belza
'''
import sys
sys.path +=sys.path + ['..']
from gwnscheduler2 import Scheduler

class gwnSimpleFDMA(Scheduler):
    '''
    '''

    def __init__(self,bandDL1,bandUL1):
        '''  
        Constructor.
        
        '''        
        super(gwnSimpleFDMA,self).__init__(1,1)        
        self.finished = False
        
    def fn_sched(self):
        '''
        '''
        in_qu = self.ports_in[0]
        if in_qu:
            if not in_qu.empty():
                event = in_qu.get()
                for q in self.ports_out[0]:
                    q.put(event,False)                
        else:
            print 'ERROR; No input queue defined'   # shows sometimes...
        return
