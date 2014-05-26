#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Thu Dec 13 14:31:45 2012

@author: belza
'''

import threading,Queue
import sys
sys.path +=sys.path + ['..']

class gwnBlock(threading.Thread):
    '''The main block. All blocks inherit from it
    '''

    def __init__(self, number_in=0,number_out=0):
        '''  
        Constructor.
        
        @param number_in: The number of input ports of this block.
        @param number_out: The number of output ports of this block.
        '''        
        threading.Thread.__init__(self)
        self.ports_in = None
        self.ports_out =None
        self.finished = False
        self.set_in_size(number_in)
        self.set_out_size(number_out)
#    def run(self):
#        pass    
    def set_in_size(self,number_in):
        self.ports_in = number_in*[None]
    def set_out_size(self,number_out):
        self.ports_out = [[] for x in xrange(number_out)]
    def get_port_in(self,index):
        return self.ports_in[index]
    def set_connection_in(self,connector,index):
        if index <= len(self.ports_in)-1:
            self.ports_in[index] = connector
    def set_connection_out(self,connector,index):        
        if index <= len(self.ports_out)-1:
            self.ports_out[index].append(connector)
    
    def stop(self):
            self.finished = True
            self._Thread__stop()

def test():
    '''A test function.
    '''
    myQueue=Queue.Queue(10)
    gwnblock =gwnBlock(5,7)
    gwnblock.set_connection_in(myQueue,3)
    gwnblock.ports_in[3].put("hola")
    print gwnblock.ports_in   
    print gwnblock.ports_in[3].get()
    gwnblock.set_connection_out(myQueue,2)
    gwnblock.ports_out[2].put("hola")
    print gwnblock.ports_out   
    print gwnblock.ports_out[2].get()
    gwnblock.set_connection_out(myQueue,9)
 
    

if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        pass


