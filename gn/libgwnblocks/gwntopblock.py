#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Thu Dec 13 14:31:45 2012

@author: belza
'''

import sys, Queue
import gwnblock  #.GWNBlock as gwn
import gwninport

sys.path +=sys.path + ['..']


# constants
debug = True

class GWNTopBlock():
    '''Defines blocks and connections.

    The main program must create an object of a class that inherits from this class. 
    In that object is where the blocks and connections are defined.
    This main can be created with Companion.
    In this class is where the function that connect two blocks is defined.
    The blocks in GNU Wireles Network musst inherit from gwmBlock because this class defines the interface and in that way can be called from this class to connect blocks.
    '''

    def __init__(self,queues_size=10):
        '''  
        Constructor.
        '''        
        self.queues_size = queues_size
        
    def connect(self, tuple1, tuple2):
         if debug:
            print tuple1
            print tuple2

         port = tuple2[0].get_port_in(tuple2[1])
         if port:
             tuple1[0].set_connection_out(port, tuple1[1])
         else:
             queue = gwninport.AQueueConnector(self.queues_size)
             tuple1[0].set_connection_out(queue, tuple1[1])
             tuple2[0].set_connection_in(queue, tuple2[1])

    def connect1(self, tuple1, tuple2):
        ''' Connects source port out to sink port in.

        source_out  ---->  sink_in
        '''
        if debug:
            print tuple1
            print tuple2

        source, source_out = tuple1
        sink, sink_in = tuple2

        #port = tuple2[0].get_port_in(tuple2[1])
        port_in = sink.get_port_in(sink_in)
        print port_in
        if port_in:
            #tuple1[0].set_connection_out(port, tuple1[1])
            sink.set_connection_out(port_in, sink_in)
        else:
            connector = gwninport.AQueueConnector(self.queues_size)

            #tuple1[0].set_connection_out(queue, tuple1[1])
            source.set_connection_out(connector, source_out)
            #tuple2[0].set_connection_in(queue, tuple2[1])
            sink.set_connection_in(queue, sink_in)
            



class top_block_test(GWNTopBlock):

	def __init__(self):
         GWNTopBlock.__init__(self)
         ##################################################
         # Blocks
         ##################################################
         self.source_0 = gwnblock.GWNBlock(1, 'BlockOne', 0, 1) 
         self.sink_0   = gwnblock.GWNBlock(2, 'BlockTwo', 1, 0) 
         ##################################################
         # Connections
         ##################################################
         self.connect( (self.source_0, 0), (self.sink_0, 0) )



def test():
    '''A test function.
    '''
    tb = top_block_test()
    print tb.source_0
    print tb.sink_0

    #tb.source_0.ports_out[0].put('Hello')
    tb.source_0.write_out(0, 'Hello')
    aux = tb.sink_0.ports_in[0].get()    
    print aux



if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        pass


