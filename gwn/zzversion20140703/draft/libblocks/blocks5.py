#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

http://www.tutorialspoint.com/python/python_multithreading.htm
'''

import threading
import Queue

import time
import sys

#import sys
#sys.path +=sys.path + ['..']

#constants
thread_lock = threading.Lock()


### classes in the framework

class Connector():
    '''A data structure to put and get events from.

    This class must be subclassed; methods put() and get() must be overwritten. This class decouples the data structure implementation. A connector may be any class that contains functions put() and get().

    The data structure will usually exhibit the behavior of a FIFO list.
    '''

    def get():
        '''Retrieves an event if there is one, None otherwise.
    
        @return: an Event object or None if the data structure is empty.
        '''
        return None

    def put(ev):
        '''Stores an event.

        @param ev: an Event object to store.
        '''
        return

    def is_empty(self):
        '''Returns True if empty, False otherwise.
        '''
        return True

    def __str__(self):
        return 'Connector instance'



class AListConnector(Connector):
    '''A Connector with a simple list as the data struture.
    '''
    def __init__(self):
        self.lsevents = []

    def get(self):
        if len(self.lsevents) > 0:
            ev = self.lsevents.pop(0)
            return ev
        else:
            return None

    def put(self, ev):
        self.lsevents.append(ev)
        return

    def is_empty(self):
        if len(self.lsevents) > 0:
            return False
        else:
            return True


class AQueueConnector(Connector):
    '''A Connector with a Queue object as the data struture.
    '''
    def __init__(self, maxsize=15):
        self.lsevents = Queue.Queue(maxsize=maxsize)

    def get(self):
        try:
            ev = self.lsevents.get(True, 1)
        except Queue.Empty:
            ev = None
        return ev

    def put(self, ev):
        try:
            self.lsevents.put(ev, True, 1)
        except Queue.Full:
            print 'QueueConnector full, event %s discarded' % (ev,)
        return

    """def is_empty(self):
        if len(self.lsevents) > 0:
            return False
        else:
            return True"""


class InPort(threading.Thread):
    '''Receives, sends and processes input events of certain types.

    @ivar accept: event types accepted in this port.
    @param conn: a Connector instance, one and only one, to receive events.
    '''
    def __init__(self, block, port_nr):
        '''Constructor.

        @param conn: a Connector instance.
        '''
        threading.Thread.__init__(self)
        self.accept = []
        #self.conn = AListConnector()
        self.conn = AQueueConnector()
        self.block = block
        self.port_nr = port_nr
        self.exit_flag = False


    def run(self):
        '''Runs InPort thread.'''
        print '  Starting InPort %d in block %s' % (self.port_nr, self.block.blkname)
        while not self.exit_flag:
            ev = self.conn.get()
            thread_lock.acquire()
            if ev:
                print '    port %d in block %s received event %s' % \
                    (self.port_nr, self.block.blkname, ev)
                self.block.process_data(self.port_nr, ev)
            thread_lock.release()
        return

    def stop(self):
        '''Stops InPort thread.'''
        print '  ...stopping port %d in block %s' % (self.port_nr, self.block.blkname)
        self.exit_flag = True
        return


    def __str__(self):
        ssaccept = ''
        for ev in self.accept:
            ssaccept += ev + ' '
        #return '%s: accepted events: %s, connector empty: %s' % \
        #     (self.__class__, ssaccept, self.conn.is_empty() )
        return  '  port %d in block %s' % (self.port_nr, self.block.blkname)


class Block(threading.Thread):
    '''Reads from input ports, processes events, writes into output ports.
    '''
    def __init__(self, blkid, blkname, qt_ports_in=0):
        threading.Thread.__init__(self)
        self.blkid = blkid
        self.blkname = blkname
        self.exitFlag = 0
        self.ports_in = []
        for i in range(0, qt_ports_in):
            port = InPort(self, i)
            print port
            self.ports_in.append(port)

    def stop(self):
        #self.exitFlag = 1
        print "Stopping " + self.blkname + '... '
        #for port in self.ports_in:
        #    port.stop()
        #for port in self.ports_in:
        #    port.join()
        for port in self.ports_in:
            port.stop()
        print self.blkname + ' stopped.'
        return

    def run(self):
        print "Starting " + self.blkname
        for port in self.ports_in:
            port.start()
        for port in self.ports_in:
            port.join()
        #self.process_data() #self.blkname, self.blkqueue)

        return

    def process_data(self, port_nr, ev):
        print 'Block %s, port %d, processing event %s...' % \
            (self.blkname, port_nr, ev),
        #print '          ', self.ports[port_nr].conn.lsevents
        time.sleep(1)
        print ' done with event %s' % (ev,)
        return

    def __str__(self):
        ss = 'Block %s, contains %d ports\n' % (self.blkname, len(self.ports_in))
        for port in self.ports_in:
            ss = ss + '  port %d in block %s\n' % (port.port_nr, port.block.blkname)
        return ss




def test1():
    '''Tests AListConnector class.
    '''
    conn = AListConnector([1,2,3,4,5,6])
    print conn.lsevents
    for i in range(0,3):
        print conn.get(),
    print
    for i in range(0,3):
        conn.put('A' + str(i))
    print conn.lsevents
    while not conn.is_empty():
        print conn.get(),
    print


def test2():
    '''Test InPort, Block classses.
    '''
    blk1 = Block(1, 'BlockOne', 2)
    print blk1

    #blk1.start()
    #time.sleep(2)

    for i in range(0,5):
        blk1.ports_in[0].conn.put('A' + str(i))
    for i in range(0,3):
        blk1.ports_in[1].conn.put('B' + str(i))
    for port in blk1.ports_in:
        print port.port_nr, port.conn.lsevents, id(port)
    #sys.exit()

    blk1.start()
    time.sleep(10)
    for i in range(5,10):
        blk1.ports_in[0].conn.put('A' + str(i))
        blk1.ports_in[1].conn.put('B' + str(i-2))
        time.sleep(2)
    time.sleep(2)
    blk1.stop()
    blk1.join()
    #blk1.stop()

        

if __name__ == '__main__':
    try:
        #test1()
        test2()
    except KeyboardInterrupt:
        pass
