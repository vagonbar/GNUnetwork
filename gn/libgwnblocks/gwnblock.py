#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Thu Dec 13 14:31:45 2012

@author: belza
'''

import threading,Queue,time
import sys

from gwninport import *   # suppress after qulifying all gwninport items
import gwninport

sys.path +=sys.path + ['..']

thread_lock = threading.Lock()



class GWNBlock(threading.Thread):
    '''The main block. All blocks inherit from it.
    '''

    def __init__(self, blkid, blkname, number_in=0,number_out=0, timers=[]):
        '''  
        Constructor.
        
        @param number_in: the number of input ports of this block.
        @param number_out: the number of output ports of this block.
        @param timers: a list of timers. TODO: may become tuples to build timers.
        '''        
        threading.Thread.__init__(self)
        self.blkid = blkid
        self.blkname = blkname
        self.ports_in = []
        self.ports_out = []
        self.timers = []
        self.finished = False
        self.set_in_size(number_in)
        self.set_out_size(number_out)
        self.set_timers(timers)


    def set_in_size(self,number_in):
        '''Creates a list of input connections.

        Creates a list of InPort instances; each InPort instances will be later assigned a Connector instance to implement the input connection.
        @param number_in: the number of input connections.
        '''
        for i in xrange(0, number_in):
            port = InPort(self, i)
            print port
            self.ports_in.append(port)


    def set_out_size(self,number_out):
        '''Creates a list of output connections.

        Creates a lists of empty lists; each of the empty lists is an output connection.
        @param number_out: the number of output connections.
        '''
        self.ports_out = [[] for x in xrange(0,number_out)]


    def set_timers(self, timers):
        '''Creates InTimer instances, assigns to block.

        TODO: construction of timers requires interval, event types (timing and stop), total run time, ...
        '''
        self.timers = timers


    def get_port_in(self,index):
        '''Returns an input port in this block.

        Returns the InPort instance assigned to this block placed in the position indicated by index.
        @param index: the position of the input port in this block.
        '''
        return self.ports_in[index]


    def get_connector_in(self,index):
        '''Returns the connector of an input port in this block.

        Returns the Connector instance assigned to the InPort instance in this block placed in the position indicated by index.
        @param index: the position of the input port in this block.
        '''
        return self.ports_in[index].conn


    def set_connection_in(self, connector, index):
        '''Sets an input connection to a port in this block.

        Assigns a Connector instance to the InPort instance in this block placed in the position indicated by indes.
        @param connector: a Connector instance.
        @param index: the position of the input port in this block.
        '''
        if index <= len(self.ports_in)-1:
            self.ports_in[index].connect(connector)


    def set_connection_out(self, connector, index):
        '''Sets an ouput connection from this block.

        A Connector instance is assigned as an output connection from this block, in the position indicated by index.
        @param connector: a reference to a Connector object.
        @param index: the position of the output port in this block.
        '''
        if index <= len(self.ports_out)-1:
            self.ports_out[index] = connector


    def write_out(self, port_nr, ev):
        '''Send (write) events on all connections of an output port.

        @param port_nr: the output por number, an index of the output ports list.
        @param ev: an Event object.
        '''
        #for q in self.ports_out[port_nr]:
        for conn in self.ports_out:
            conn.put(ev)

            
    def run(self):
        '''Run this thread.'''
        print "Starting " + self.blkname
        for port in self.ports_in:
            port.start()
        for port in self.ports_in:
            port.join()

        for timer in self.timers:
            timer.start()
        for timer in self.timers:
            timer.join()
        return


    def stop(self):
        '''Stops ports, timers, then stops block.
        '''
        #self.exitFlag = 1
        print "Stopping " + self.blkname + '... '
        for port in self.ports_in:
            port.stop()
        for timer in self.timers:
            timer.stop()
        print self.blkname + ' stopped.'
        return

        


    ### user defined process code
    ###
    def process_data(self, port_nr, ev):
        '''Block specific processing.

        @param port_nr: the port number on which the event was received.
        @param ev: an Event object.
        '''
        print 'Processing, block %s, port %d, event %s... ' % \
            (self.blkname, port_nr, ev),
        #print '          ', self.ports[port_nr].conn.lsevents
        #time.sleep(1)
        #print ' done with event %s' % (ev,)
        print 'done.'
        return
    ###
    ### end user defined process code


    def __str__(self):
        ss = 'Block %s, %d in_ports, %d out_ports, %d timers\n' % \
            (self.blkname, len(self.ports_in), len(self.ports_out), len(self.timers))
        for port in self.ports_in:
            ss = ss + '  in_port %d in block %s\n' % (port.port_nr, port.block.blkname)
        for i in range(len(self.ports_out)):   # no port_nr in ports_out
            ss = ss + '  out_port %d in block %s\n' % \
                (i, self.ports_out[i])
        for timer in self.timers:
            ss = ss + '  timer %d in block %s\n' % (timer.port_nr, timer.block.blkname)
        return ss



### tests


# a single block test

def test2():
    '''Test InPort, Block classses.
    '''
    blk1 = GWNBlock(1, 'BlockOne', 2)
    print blk1
    connector1 = AQueueConnector()
    connector2 = AQueueConnector()
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
    time.sleep(10)
    for i in range(5,10):
        connector1.put('A' + str(i))
        connector2.put('B' + str(i-2))
        time.sleep(2)
    time.sleep(2)
    blk1.stop()
    blk1.join()
    #blk1.stop()


# two block test

class BlockCopy(GWNBlock):
    '''Copies event from input into output.
    '''
    def process_data(self, port_nr, ev):
        print '\nCopying, block %s, port %d, event %s... ' % \
            (self.blkname, port_nr, ev),
        self.write_out(0, ev)
        print 'done.'
        return

class BlockReceive(GWNBlock):
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



if __name__ == '__main__':
    try:
        #test2()
        test3()
    except KeyboardInterrupt:
        pass


