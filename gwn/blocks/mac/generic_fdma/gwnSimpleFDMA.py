#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Thu Dec 13 14:31:45 2012

@author: belza
'''
import sys, threading
sys.path +=sys.path + ['..']
import libgwnBlocks.gwnBlock as gwn

class SimpleFDMA(gwn.GWNBlock):
    '''
    '''

    def __init__(self,bandDL1,bandUL1):
        '''  
        Constructor.
        
        '''        
        super(SimpleFDMA, self).__init__(1, 'SimpleFDMA', 2, 2)
        self.finished = False
        
    def run(self):
        '''
        '''
        self.ul = self.ReadUL(self.ports_in[1],self.ports_out[1])
        self.ul.start()  
        while not self.finished :              
            in_qu = self.ports_in[0]
            event = in_qu.get()
            for q in self.ports_out[0]:
                q.put(event,False)                
        return

    def stop(self):        
        self.ul.stop()
        self.finished = True
        self._Thread__stop()

        
        
    class ReadUL(threading.Thread):
        '''Subclass of Scheduler for adapting layers 3 and 2.
        '''
        
        def __init__(self,in_queue,out_queues):
            '''  
            Constructor
            
            '''
            threading.Thread.__init__(self)
            self.in_queue = in_queue
            self.out_queues = out_queues
            self.finished = False            
            
        def run(self):
            ''' reads events, outputs frames.
            '''
            while not self.finished :
                event = self.in_queue.get()
                for q in self.out_queues:
                    q.put(event)
            return
        def stop(self):
            self.finished = True
            self._Thread__stop()


