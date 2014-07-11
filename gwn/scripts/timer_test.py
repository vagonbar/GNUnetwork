#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun May 18 19:16:28 2014

@author: belza
"""
import sys
sys.path +=sys.path + ['..']
import libgwnBlocks.gwnTopBlock as gwnTB
import libvirtualchannel.EventConsumer2 as consumer
import libvirtualchannel.EventSimulator2 as simulator
import libtimer.timer2 as timer



class top_block_test(gwnTB.gwnTopBlock):

    def __init__(self):
        gwnTB.gwnTopBlock.__init__(self)
        ##################################################
        # Blocks
        ##################################################
        self.timer_0 =timer.Timer(0.5,3,"TimerTOR1",None,"TimerTOR2") 
        self.sink_0 = consumer.EventConsumer("Consumer 1")
        self.source_0 = simulator.EventSimulator("TimerConfig","3.3","2","TimerTimer")
        self.timer_1 =timer.Timer(10,4,"TimerTimer") 

        ##################################################
        # Connections
        ##################################################
        self.connect((self.timer_0, 0), (self.sink_0, 0))
        self.connect((self.timer_1, 0), (self.source_0, 0))
        self.connect((self.source_0, 0),(self.timer_0, 0))

def test():
    '''A test function.
    '''
    tb= top_block_test()
    tb.timer_0.start()
    tb.timer_1.start()
    tb.source_0.start()
    tb.sink_0.start()
    
    
    tb.timer_1.join()
    tb.sink_0.stop()
    tb.source_0.stop()
    tb.timer_0.stop()
    
    print "program ends"
    

if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        pass
