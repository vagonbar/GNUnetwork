#!/usr/bin/env python
# -*- coding: utf-8 -*-


import gwnBlock
from gwnBlock import thread_lock

import time

class InPortTimer(gwnBlock.InPort):
    '''A timer event genrator.
    '''
    def __init__(self, block, port_nr, interval=1):
        '''Constructor.

        @param interval: time to sleep.
        '''
        gwnBlock.InPort.__init__(self, block, port_nr)
        self.interval = interval
        self.counter = 0

    def run(self):
        '''Runs InPort thread, generates events regularly.'''
        print '  Starting InPortTimer %d in block %s' % (self.port_nr, self.block.blkname)
        while not self.exit_flag:
            ev = 'TimeEv %s %d : %d' % (self.block.blkname, self.port_nr, self.counter)
            self.counter += 1
            #if ev:
            thread_lock.acquire()
            #print '    port %d in block %s generated event %s' % \
            #    (self.port_nr, self.block.blkname, ev)
            print '   %s' % (ev,)
            self.block.process_data(self.port_nr, ev)
            thread_lock.release()
            time.sleep(self.interval)
        return


def test2():
    '''Test InPort, Block classses.
    '''
    blk1 = gwnBlock.gwnBlock(1, 'BlockTimer', 2)
    print blk1
    #connector1 = AQueueConnector()
    #connector2 = AQueueConnector()
    #blk1.start()
    #time.sleep(2)
    #blk1.set_connection_in(connector1,0)
    #blk1.set_connection_in(connector2,1)
    

    # set_in_size() done here for InPortTimer 
    for i in xrange(0, len(blk1.ports_in)):
        port = InPortTimer(blk1, i, 1)
        print port
        blk1.ports_in[i] = port

    """
    for i in range(0,5):
        connector1.put('A' + str(i))
    for i in range(0,3):
        connector2.put('B' + str(i))
    for port in blk1.ports_in:
        print port.port_nr, port.conn.lsevents, id(port)
    #sys.exit()
    """

    blk1.start()
    time.sleep(10)
    """
    for i in range(5,10):
        connector1.put('A' + str(i))
        connector2.put('B' + str(i-2))
        time.sleep(2)
    time.sleep(2)
    """
    blk1.stop()
    blk1.join()
    #blk1.stop()

if __name__ == '__main__':
    try:
        test2()
    except KeyboardInterrupt:
        pass