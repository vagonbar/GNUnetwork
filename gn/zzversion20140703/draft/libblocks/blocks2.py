#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
An experimental block implementation.

Each block has a single "input queue", and several "input ports". All events are received and queued in the input queue. When an event is got from the input queue, it is handed to all input ports. Ideally, only one input port understands it and processes accordingly; the rest ignore the event.

Input ports are objects, and so can retain state and exhibit behavior. The state and behavior of input ports are the "customizable" part of input port objects. Input port objects are instances of a subclass or the InPort (abstract) class.

New functionaliites are added in the input ports. A programmer needs only to subclass the InPort class and write the processing code in the subclass; the new input port is then attached to an instance of the Block class. The Block class need not be touched nor subclassed (though it may be).

The test:  an RTS - CTS - Data - ACK dialog between two blocks.

The blocks and ports:

           Block1                   Block2
             InPortSend1 ------------> block 2 input queue
events --->  block 1 input queue <---- InPortReceive1
             InportConf1

Block 1 receives in its input queue a sequence of events, which may be Configuration, Data, CTS, ACK or other. Port InPortConf1 understands configuration events Conf, Reset, and discards others; port InportSend1 understands Data, CTS, ACK events and discards others. Processing invoked by InPortSend1 can send RTS and Data.

Block 2 receives events from Block 1 in its input queue; InPortReceive1 understands RTS, Data, events, and discards others. Processing invoked by InPortReceive1 can send CTS and ACK.

Nomenclature "InPort..." may be confusing; object acts as an input port, but invokes processing which may be creating and sending events.

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

    This class must be considered abstract; working input ports are expected to be instances of a subclass of this class.

    TODO: see if inportid, inportname are necessary.
    @ivar inportid: identifier, an integer.
    @ivar inportname: name, a string.
    @ivar accept: event types accepted in this port.
    @ivar lsevents: a list of received events to process.
    @ivar waitfor: an element or list to recognize an event or state waited for.
    '''
    def __init__(self, inportid, inportname):
        '''Constructor.
        '''
        self.inportid = inportid
        self.inportname = inportname
        #self.myblock = None
        self.accept = []
        self.waitfor = None
        self.lsevents = []


    def process_event():
        '''Processes events in this port.

        This function must be overwritten.
        '''
        pass
        return


    def __str__(self):
        ssaccept = ''
        for ev in self.accept:
            ssaccept += ev + ' '
        return '%s: %s, %d\n   accepted events: %s' % \
             (self.__class__, self.inportname, self.inportid, ssaccept)



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

    def __init__(self, blkid, blkname, in_ports, out_blocks=None, \
            maxqueue=10):
        '''Constructor.

        @param maxqueue: size of block input queue.
        '''
        threading.Thread.__init__(self)
        self.blkid = blkid
        self.blkname = blkname
        self.blkqueue = Queue.Queue(maxqueue)
        self.exit_flag = 0
    	self.in_ports = in_ports
        self.out_blocks = out_blocks


    def stop(self):
        '''To stop thread.
        '''
        self.exit_flag = 1


    def run(self):
        '''To run thread.

        Decouples data processing in this thread.
        '''
        print "Starting " + self.blkname
        self.process_data() #self.blkname, self.blkqueue)
        print "Exiting " + self.blkname


    def writeout(self, lsret):
        if self.out_blocks:
            for ev in lsret:
                for block in self.out_blocks:
                    block.blkqueue.put(ev)
        return


    def process_data(self):   #blkname, blkqueue):
        '''How this block handles input events.

        Extracts an event from the common input queue, puts this event into each of the input ports lists, and invokes the processing of each input port.

        TODO: input queue lock perhaps not necessary.
        @return: a list of events to transmit (send) to other blocks.
        '''
        while not self.exit_flag:
            queueLock.acquire()
            if not self.blkqueue.empty():
                event_in = self.blkqueue.get()
                queueLock.release()
                print "%s received %s" % \
                    (self.blkname, event_in)

                # process each in_port list
                for port in self.in_ports:
                    port.lsevents.append(event_in)
                    lsret = port.process_event()
                    self.writeout(lsret)
                """
                # verify if event is in list of accepted events
                # NOT WORKING, perhaps not necessary
                for port in self.in_ports:
                    if event_in in port.accept:
                        port.lsevents.append(event_in)
                    else:
                        continue
                else:
                    print "   %s not accepted in port %d!" % \
                        (event_in, port.inportid)
                    print port.inportid, port.accept, event_in
                    del event_in
                """
            else:
                print "    %s idle" % (self.blkname,)
                queueLock.release()
            time.sleep(1)
        return


    def send(self, event_out):
        '''Puts event in input queues of out blocks.

        @param event_out: an event to output.
        '''
        if self.out_blockss:
            for block in self.out_blocks:
                block.blkqueue.put(event_out)

    def __str__(self):
        return '%s: %s, %d' % \
            (self.__class__, self.blkname, self.blkid)



### Classes for Testing

class InPortSend(InPort):
    '''Receives data and control to send data to other blocks.

    @ivar data_buf: a buffer to retain data while negotiating connection.
    '''
    def __init__(self, inportid, inportname, accept):
        InPort.__init__(self, inportid, inportname)
        self.accept = accept
        ### begin customize
        self.waitfor = 'Data'
        self.data_buf = ''
        ### end customize
        return

    def process_event(self):
        '''Processes events according to this input port function.
        '''
        lsret = []   # the list of events to return
        if len(self.lsevents) > 0:        # input list not empty
            ev = self.lsevents.pop()      # extract first event

            ### begin customize
            if 'Data' in ev and 'Data' in self.waitfor:
                print '  %s %d received %s, sending RTS >>>' % \
                    (self.inportname, self.inportid, ev)
                self.data_buf = ev     # keep data in buffer to send
                lsret.append('RTS')    # event to send
                self.waitfor = 'CTS'   # event to wait for
            elif 'CTS' in ev and 'CTS' in self.waitfor:
                print '  %s %d received %s, sending %s >>>' % \
                    (self.inportname, self.inportid, ev, self.data_buf)
                lsret.append(self.data_buf)  # send data in buffer
                self.waitfor = 'ACK'   # event to wait for
            elif 'ACK' in ev and 'ACK' in self.waitfor:
                print '  %s %d received %s, waits for new data' % \
                    (self.inportname, self.inportid, ev)
                self.data_buf = ''     # data received OK
                self.waitfor = 'Data'  # event to wait for
            else:
                print '  %s %d received unknown, discard: %s' % \
                    (self.inportname, self.inportid, ev)
            ### end customize

        else:    # event is not recognized by this input port
            pass
        return lsret


class InPortReceive(InPort):
    '''Receives data from other block(s).
    '''
    def __init__(self, inportid, inportname, accept):
        InPort.__init__(self, inportid, inportname)
        self.accept = accept
        ### begin customize        
        self.waitfor = 'RTS'
        ### end customize
        return

    def process_event(self):
        '''Processes events according to this input port function.
        '''
        lsret = []   # the list of events to return
        if len(self.lsevents) > 0:        # input list not empty
            ev = self.lsevents.pop()      # extract first event

            ### begin customize
            if 'RTS' in ev and 'RTS' in self.waitfor:
                print '  %s %d received %s, sending CTS >>>' % \
                    (self.inportname, self.inportid, ev)
                lsret.append('CTS')    # event to send
                self.waitfor = 'Data'  # event to wait for
            elif 'Data' in ev and 'Data' in self.waitfor:
                print '  %s %d received %s, sending ACK >>>' % \
                    (self.inportname, self.inportid, ev)
                lsret.append('ACK')    # event to send
                self.waitfor = 'RTS'   # event to wait for
            else:
                print '  %s %d received unknown, discard: %s' % \
                    (self.inportname, self.inportid, ev)
            ### end customize

        else:
            pass
        return lsret



class InPortConf(InPort):
    '''Receives configuration for this block.
    '''
    def __init__(self, inportid, inportname, accept):
        InPort.__init__(self, inportid, inportname)
        self.accept = accept
        ### begin customize
        self.waitfor = ['Conf', 'Reset']
        ### end customize
        return

    def process_event(self):
        '''Processes events according to this input port function.
        '''
        lsret = []   # the list of events to return
        if len(self.lsevents) > 0:        # input list not empty
            ev = self.lsevents.pop()      # extract first event

            ### begin customize
            if ev in self.waitfor:
                print '  %s %d received %s, sending OK >>>' % \
                    (self.inportname, self.inportid, ev)
                lsret.append('OK')
            else:
                print '  %s %d received unknown, discard: %s' % \
                    (self.inportname, self.inportid, ev)
            ### end customize
        return lsret


### testing

def test():

    print '=== construction ==='

    inp3 = InPortReceive(3, 'InPortReceive1', ['RTS', 'Data'])
    print inp3
    blk2 = Block(2, 'Block2', [inp3], out_blocks=[])
    print blk2
    print

    inp1 = InPortSend(1, 'InPortSend1', ['Data', 'CTS', 'ACK'])
    print inp1
    inp2 = InPortConf(2, 'InPortConf1', ['Conf', 'Reset'])
    print inp2
    blk1 = Block(1, 'Block1', [inp1, inp2], out_blocks=[blk2])
    print blk1

    blk2.out_blocks = [blk1]    # block 2 back to 1 for CTS, ACK

    print


    print '=== run ==='
    blk1.start()
    blk2.start()

    lsevents = ['Data 1', 'ev1', 'Data 2', 'Conf', 'Data 3']
    for ev in lsevents:
        blk1.blkqueue.put(ev)
        time.sleep(3)


    #blk2 = Block(2, 'Block Two', Queue.Queue(10))
    #blk2.start()

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
