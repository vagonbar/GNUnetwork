#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Thu Dec 13 14:31:45 2012

@author: belza
'''

import threading, Queue,time
import sys
sys.path += sys.path + ['..']

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
    @ivar conn: a Connector instance, one and only one, to receive events.
    @ivar block: the block to which this instance is attached.
    @ivar port_nr: the "port number" assigned to this instance; it it an index in the list of timers in the container block.
    @ivar exit_flag: set to True to stop thread, default False.
    '''
    def __init__(self, block, port_nr):
        '''Constructor.
        '''
        threading.Thread.__init__(self)
        self.accept = []
        #self.conn = AListConnector()
        self.conn = None
        self.block = block
        self.port_nr = ("inport",port_nr)
        self.exit_flag = False


    def connect(self, connector):
        '''Assigns a Connector objec to this InPort.

        @param connector: a Connector object.
        '''
        self.conn=connector


    def run(self):
        '''Runs thread.'''
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
        '''Stops thread.'''
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



