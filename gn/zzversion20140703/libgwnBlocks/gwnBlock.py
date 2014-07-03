#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Thu Dec 13 14:31:45 2012

@author: belza
'''

import threading,Queue,time
import sys
sys.path +=sys.path + ['..']

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
        self.conn = None
        self.block = block
        self.port_nr = port_nr
        self.exit_flag = False

    def connect(self, connector):
        self.conn=connector

    def run(self):
        '''Runs InPort thread.'''
        print '  Starting InPort %d in block %s' % (self.port_nr, self.block.blkname)
        while not self.exit_flag:
            ev = self.conn.get()
            if ev:
                thread_lock.acquire()
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


class gwnBlock(threading.Thread):
    '''The main block. All blocks inherit from it.
    '''

    def __init__(self, blkid, blkname, number_in=0,number_out=0):
        '''  
        Constructor.
        
        @param number_in: the number of input ports of this block.
        @param number_out: the number of output ports of this block.
        '''        
        threading.Thread.__init__(self)
        self.blkid = blkid
        self.blkname = blkname
        self.ports_in = []
        self.ports_out =None
        self.finished = False
        self.set_in_size(number_in)
        self.set_out_size(number_out)

#    def run(self):
#        pass    

    def set_in_size(self,number_in):
        '''Creates a list of input connections.

        Creates a list of empty items; each of the empty items will be later replaced by a list acting as an input connection.
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

    def get_port_in(self,index):
        '''Returns an input list to this block.

        Returns the input list to this block placed in the position indicated by index.
        @param index: the position of the input list to return.
        '''
        return self.ports_in[index]

    def set_connection_in(self,connector,index):
        '''Sets an input connection to this block.

        The connector, a list, is assigned as an input connection to this block in the position indicated by index.
        @param connector: a reference to a list.
        @param index: a position in ports_in.
        '''
        if index <= len(self.ports_in)-1:
            self.ports_in[index].connect(connector)

    def set_connection_out(self,connector,index):
        '''Sets an ouput connection to this block.

        The connector, a list, is assigned as an output connection to this block in the position indicated by index.
        @param connector: a reference to a list.
        @param index: a position in ports_in.
        '''
        if index <= len(self.ports_out)-1:
            self.ports_out[index].append(connector)
    
    def stop(self):
        #self.exitFlag = 1
        print "Stopping " + self.blkname + '... '
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
        
    def write_out(self, index,ev):
        for q in self.ports_out[index]:
            q.put(ev)



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



def test2():
    '''Test InPort, Block classses.
    '''
    blk1 = gwnBlock(1, 'BlockOne', 2)
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

 
    

if __name__ == '__main__':
    try:
        test2()
    except KeyboardInterrupt:
        pass


