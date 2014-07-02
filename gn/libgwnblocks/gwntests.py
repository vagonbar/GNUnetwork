#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''GWN Blocks tests.
'''

import time
import sys

import gwnblock
import gwninport
import gwntimer



###
### a single block test
###

def test2():
    '''Test InPort, Block classses.
    '''
    blk1 = gwnblock.GWNBlock(1, 'BlockOne', 2)
    print blk1
    connector1 = gwninport.AQueueConnector()
    connector2 = gwninport.AQueueConnector()
    #blk1.start()
    #time.sleep(2)
    blk1.set_connection_in(connector1,0)
    blk1.set_connection_in(connector2,1)
    
    for i in range(0,5):
        connector1.put('A' + str(i))
    for i in range(0,3):
        connector2.put('B' + str(i))
    for port in blk1.ports_in:
        print port.port_nr, port.conn.lsevents, id(port)
    #sys.exit()

    blk1.start()
    time.sleep(8)
    for i in range(5,10):
        connector1.put('A' + str(i))
        connector2.put('B' + str(i-2))
        time.sleep(2)
    time.sleep(2)
    blk1.stop()
    blk1.join()
    #blk1.stop()



###
### two block test
###

class BlockCopy(gwnblock.GWNBlock):
    '''Copies event from input into output.
    '''
    def process_data(self, port_nr, ev):
        print '\nCopying, block %s, port %d, event %s... ' % \
            (self.blkname, port_nr, ev),
        self.write_out(0, ev)
        print 'done.'
        return


class BlockReceive(gwnblock.GWNBlock):
    '''Receives an event, informs.
    '''
    def process_data(self, port_nr, ev):
        print 'Received, block %s, port %d, event %s... ' % \
            (self.blkname, port_nr, ev),
        #self.write_out(0, ev)
        print 'done.'
        return


def test3():
    '''Tests connection from one block to another block.
    '''
    blk1 = BlockCopy(1, 'BlkCopy', 1, 1)
    blk2 = BlockReceive(1, 'BlkReceive', 1, 0)

    conn1 = gwninport.AQueueConnector(10)
    conn2 =  gwninport.AQueueConnector(10)
    blk1.set_connection_in(conn1,0)
    blk2.set_connection_in(conn2,0)
    blk1.set_connection_out(conn2, 0)

    print blk1
    print blk2

    blk1.start()
    blk2.start()

    for i in range(0,5):
        conn1.put('A' + str(i))
        time.sleep(1)

    #blk1.ports_in[0].conn.put('EventA1')

    blk1.stop()
    blk2.stop()
    blk1.join()
    blk2.join()



###
### a block with timer
###

class BlockTimerCopy(gwnblock.GWNBlock):
    '''Copies event from input into output, outputs events from timer.
    '''
    def process_data(self, port_nr, ev):
        print '\nEvent, block %s, port %d, event %s... ' % \
            (self.blkname, port_nr, ev),
        self.write_out(0, ev)
        print 'done.'
        return


def test4():
    '''Block with input ports, output ports and timer.
    '''

    timer0 = gwntimer.InTimer(None, 0, 1)

    blk1 = BlockCopy(1, 'BlkCopy', 1, 1, [])
    timer0.block, timer0.port_nr = blk1, 0
    blk1.set_timers([timer0])

    # same code as test 3

    blk2 = BlockReceive(1, 'BlkReceive', 1, 0)
    conn1 = gwninport.AQueueConnector(10)
    conn2 =  gwninport.AQueueConnector(10)
    blk1.set_connection_in(conn1,0)
    blk2.set_connection_in(conn2,0)
    blk1.set_connection_out(conn2, 0)

    blk1.start()
    blk2.start()

    for i in range(0,5):
        conn1.put('A' + str(i))
        time.sleep(2)

    time.sleep(4)
    blk1.stop()
    blk2.stop()
    blk1.join()
    blk2.join()


    return


if __name__ == '__main__':


    if len(sys.argv) > 1:
        if sys.argv[1] == '2':
            test = test2
        elif sys.argv[1] == '3':
            test = test3
        elif sys.argv[1] == '4':
            test = test4
    else:
        test = test3        
    try:
        test()
    except KeyboardInterrupt:
        pass