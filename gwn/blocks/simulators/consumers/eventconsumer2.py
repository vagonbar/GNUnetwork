#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 12/02/2014

@author: ggomez
'''

import sys
import time

#sys.path += ['..']
import gwnblocks.gwnblock as gwnblock
import gwnblocks.gwninport as gwninport


class EventConsumer(gwnblock.GWNBlock) :
    '''An event consumer block.
    '''

    def __init__(self, blkname):
        '''Constructor.
        
        @param nickname: '''
        super(EventConsumer,self).__init__(1, 'EventConsumer', 1, 0)
        self.blkname = blkname
        
    def process_data(self, port_type, port_nr, ev):
        '''This is the private thread that generates.
        '''
        if port_type == "inport":
  		    #print '--> Consumer %s received event %s' % (self.blkname, ev.__str__())
            print '--> Consumer', self.blkname, 'received event', ev


def test():
    blk1 = EventConsumer('consumer1')
    print blk1
    connector1 = gwninport.AQueueConnector()
    blk1.set_connection_in(connector1, 0)

    blk1.start()
    time.sleep(2)

    for i in xrange(0, 5):
        print connector1.put('ev' + str(i))
        time.sleep(1)

    time.sleep(8)
    blk1.stop()
    blk1.join()



if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        pass