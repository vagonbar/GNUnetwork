#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
An experimental block implementation.

Each block has a single "input queue", and several "input ports". All events are received and queued in the input queue. When an event is got from the input queue, it is handed to all input ports. Ideally, only one input port understands it and accepts it; the rest ignore the event.

Input ports are objects, and so can retain state, but do not exhibit behavior. Processing of events in the input lists is done by the 

The test:  an RTS - CTS - Data - ACK dialog between two blocks.

The blocks and ports:

           Block1                   Block2
             in_port 0 ------------> block 2 input queue
events --->  block 1 input queue <---- in_port 0
             in_port 1

Block 1 receives in its input queue a sequence of events, which may be Configuration, Data, CTS, ACK or other. Port 1 accepts configuration events Conf, Reset, and discards others; processing events on port 1 can send OK events. Port 0 accepts Data, CTS, ACK events and discards others; processing events on port 0 can send RTS, Data.

Block 2 receives events from Block 1 in its input queue; port 0 accepts RTS, Data events, and discards others; processing events on port 0 can send CTS, ACK.


Tutorial on threads and queues (very basic but clear):
  http://www.tutorialspoint.com/python/python_multithreading.htm
'''

import threading
import Queue

import time

#import sys
#sys.path +=sys.path + ['..']

#constants
queueLock = threading.Lock()


### classes in the framework

class InPort():
    '''Receives, sends and processes input events of certain types.

    @ivar accept: event types accepted in this port.
    @ivar lsevents: a list of received events to process.
    @ivar waitfor: an event or list to recognize an event or state waited for.
    @ivar data_buf: a list for temporal storage.
    '''
    def __init__(self):
        '''Constructor.
        '''
        self.accept = []
        self.waitfor = None
        self.lsevents = []
        self.data_buf = ''

    def __str__(self):
        ssaccept = ''
        for ev in self.accept:
            ssaccept += ev + ' '
        return '%s: accepted events: %s' % \
             (self.__class__, ssaccept)



class Block(threading.Thread):
    '''A block to contain input ports, process functions and output.

    A block contains some input blocks which can receive and process events.

    TODO: 1) names of functions must be normalized; 2) see if blkid, blkname are necessary.
    @ivar blkid: block identifier, an integer.
    @ivar blkname: block name, a string.
    @ivar blkqueue: the unique common input queue.
    @ivar exit_flag
    @param in_ports: a list of input port objects.
    @param out_blocks: a list of references to blocks; output events will be put in the input queues of these blocks.
    '''

    def __init__(self, blkid, blkname, qt_in_ports, out_blocks=None, \
            maxqueue=10):
        '''Constructor.

        @param maxqueue: size of block input queue.
        '''
        threading.Thread.__init__(self)
        self.blkid = blkid
        self.blkname = blkname
        self.blkqueue = Queue.Queue(maxqueue)
        self.exit_flag = 0
        self.in_ports = []
        self.out_blocks = out_blocks
        # create input ports
        for i in range(0,qt_in_ports):
            self.in_ports.append(InPort())


    def stop(self):
        '''To stop thread.
        '''
        self.exit_flag = 1


    def run(self):
        '''To run thread.

        Decouples data processing in this thread.
        '''
        print "Starting " + self.blkname

        while not self.exit_flag:
            queueLock.acquire()
            if not self.blkqueue.empty():
                event_in = self.blkqueue.get()
                queueLock.release()
                print "%s received %s" % \
                    (self.blkname, event_in)

                for port in self.in_ports:
                    port.lsevents.append(event_in)
            else:
                print "    %s idle" % (self.blkname,)
                queueLock.release()

            self.process_data()
            #self.writeout(lsret)
            time.sleep(1)

        print "Exiting " + self.blkname


    def writeout(self, lsret):
        '''Puts output events in input queues of next blocks.

        @param lsret: events to output.
        '''
        if self.out_blocks:
            for ev in lsret:
                for block in self.out_blocks:
                    block.blkqueue.put(ev)
        return


    def process_data(self):
        '''Do the work.

        This function must be overwritten.
        '''
        return


    def __str__(self):
        return '%s: %s, %d' % \
            (self.__class__, self.blkname, self.blkid)



### Classes for Testing

class TransmitBlock(Block):
    '''A block to transmit events.

    input port 1 receives data and control.
    input port 2 receives configuration.
    '''
    def __init__(self, blkid, blkname, qt_in_ports, out_blocks):
        Block.__init__(self, blkid, blkname, qt_in_ports, out_blocks)

        # iniitialization, can be done from __init__ if
        #    qt_in_ports becomes a list of tuples, for example
        self.in_ports[0].waitfor = ['Data']
        self.in_ports[1].waitfor = ['Conf', 'Reset']

    def process_data(self):
        ev_out = None
        # read and process input port 0
        if len(self.in_ports[0].lsevents) > 0:
            ev = self.in_ports[0].lsevents.pop()
            # the "state machine"
            if 'Data' in ev and 'Data' in self.in_ports[0].waitfor:
                self.in_ports[0].data_buf = ev
                ev_out, self.in_ports[0].waitfor = 'RTS', 'CTS'
            elif 'CTS' in ev and 'CTS' in self.in_ports[0].waitfor:
                ev_out, self.in_ports[0].waitfor = \
                    self.in_ports[0].data_buf, 'ACK'
            elif 'ACK' in ev and 'ACK' in self.in_ports[0].waitfor:
                ev_out, self.in_ports[0].waitfor = \
                    None, 'Data'
            print '  %s port %d received %s, sending %s >>>' % \
                (self.blkname, 0, ev, ev_out)
            if ev_out:
                self.writeout([ev_out])

        # read and process input port 1
        ev_out = None
        if len(self.in_ports[0].lsevents) > 0:
            ev = self.in_ports[0].lsevents.pop()
            # the "state machine"
            if 'Conf' in ev and 'Conf' in self.in_ports[0].waitfor:
                ev_out = 'OKconf'
            elif 'Reset' in ev and 'Reset' in self.in_ports[0].waitfor:
                ev_out = 'OKreset'
            print '  %s port %d received %s, sending %s >>>' % \
                (self.blkname, 0, ev, ev_out)
            if ev_out:
                self.writeout([ev_out])
        return


class ReceiveBlock(Block):
    def __init__(self, blkid, blkname, qt_in_ports, out_blocks):
       Block.__init__(self, blkid, blkname, qt_in_ports, out_blocks)

       # iniitialization, can be done from __init__ if
       #    qt_in_ports becomes a list of tuples, for example
       self.in_ports[0].waitfor = ['RTS']

    def process_data(self):
        ev_out = None
        # read and process input port 0
        if len(self.in_ports[0].lsevents) > 0:
            ev = self.in_ports[0].lsevents.pop()
            # the "state machine"
            if 'RTS' in ev and 'RTS' in self.in_ports[0].waitfor:
                ev_out, self.in_ports[0].waitfor = 'CTS', 'Data'
            elif 'Data' in ev and 'Data' in self.in_ports[0].waitfor:
                ev_out, self.in_ports[0].waitfor = 'ACK', 'RTS'
            print '  %s port %d received %s, sending %s >>>' % \
                (self.blkname, 0, ev, ev_out)
            if ev_out:
                self.writeout([ev_out])
        return

### testing

def test():

    print '=== construction ==='


    blk1 = TransmitBlock(1, 'TransmitBlock', 2, out_blocks=[])
    print blk1
    print
    blk2 = ReceiveBlock(2, 'ReceiveBlock', 1, out_blocks=[blk1])
    blk1.out_blocks = [blk2]
    print blk2
    print

    print '=== run ==='
    blk1.start()
    blk2.start()

    lsevents = ['Data 1', 'ev1', 'Data 2', 'Conf', 'Data 3']
    for ev in lsevents:
        blk1.blkqueue.put(ev)
        time.sleep(3)

    time.sleep(2)    # to finish completely, because of sleep in blocks
    blk1.stop()
    blk2.stop()
    blk1.join()
    blk2.join()
    return


if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        pass
