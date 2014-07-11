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
import libtimer.timer2 as timer
import time



class top_block_test(gwnTB.gwnTopBlock):

    def __init__(self):
        gwnTB.gwnTopBlock.__init__(self)
        ##################################################
        # Blocks
        ##################################################
        self.timer_0 =timer.Timer(0.5,10,"TimerTOR1",None,"TimerTOR2") 
        self.sink_0 = consumer.EventConsumer("New") 
        ##################################################
        # Connections
        ##################################################
        self.connect((self.timer_0, 0), (self.sink_0, 0))


def test():
    '''A test function.
    '''
    tb= top_block_test()
    tb.timer_0.start()
    tb.sink_0.start()
    
    tb.timer_0.join()
    time.sleep(5)
    tb.sink_0.stop()

if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        pass


