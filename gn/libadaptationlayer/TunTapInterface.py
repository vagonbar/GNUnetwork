#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# sched-bytype.py
#


'''A layer 3 to layer 2 Interface.

Gets a payload from a Layer 3 operating system, generates the corresponding event, and puts it into the Layer 2 queue.
Gets an event from a Layer 2 input queue, extracts the payload, and puts it into the Layer 2 event queue.
Uses the TUN/TAP Interface

'''
import Queue
import sys
sys.path +=['..']

# The next import is defined only for test
import libevents.if_events as if_events
import libgwnBlocks.gwnBlock as gwn
import os,struct,threading
import libutils.gnlogger as gnlogger
import logging
module_logger = logging.getLogger(__name__)

# ////////////////////////////////////////////////////////////////////
#
#   Use the Universal TUN/TAP device driver to move packets to/from
#   kernel
#
#   See /usr/src/linux/Documentation/networking/tuntap.txt
#
# ////////////////////////////////////////////////////////////////////

# Linux specific...
# TUNSETIFF ifr flags from <linux/tun_if.h>

IFF_TUN		= 0x0001   # tunnel IP packets
IFF_TAP		= 0x0002   # tunnel ethernet frames
IFF_NO_PI	= 0x1000   # don't pass extra packet info
IFF_ONE_QUEUE	= 0x2000   # beats me ;)

def open_tun_interface(tun_device_filename):
    from fcntl import ioctl
    
    mode = IFF_TAP | IFF_NO_PI
    TUNSETIFF = 0x400454ca

    tun = os.open(tun_device_filename, os.O_RDWR)
    ifs = ioctl(tun, TUNSETIFF, struct.pack("16sH", "gr%d", mode))
    ifname = ifs[:16].strip("\x00")
    return (tun, ifname)
    
class TunTapInterface(gwn.gwnBlock):
    '''Subclass of Scheduler for adapting layers 3 and 2.
    '''
    
    def __init__(self,device,my_addr,dst_addr):
        '''  
        Constructor
        
        '''
        super(TunTapInterface,self).__init__(1,1)        

        self.my_addr = my_addr
        self.logger = logging.getLogger(str(self.__class__))
        self.logger.debug(str(self.my_addr)+ '.... creating an instance of Layer 3 with virtual interfase')
        self.dst_addr = dst_addr
        self.device = device
        (self.tun_fd, self.tun_ifname) = open_tun_interface(device)
        self.finished = False
        print
        print "Allocated virtual ethernet interface: %s" % (self.tun_ifname,)
        print "You must now use ifconfig to set its IP address. E.g.,"
        print
        print "  $ sudo ifconfig %s 192.168.200.1" % (self.tun_ifname,)
        print
        print "Be sure to use a different address in the same subnet for each machine."
        print
        
    def run(self):
        '''Scheduling function, reads events, outputs events.
        
        Reads one element from the input event queue, and puts the event in the output queue.
        out_queues: a dictionary of {nm_queue: (out_queue)}; nm_queue is a name for the queue, out_queue is the output queue.
        Initialices a thread that read data from layer 2 and send it to the os.
        '''
        
        self.sch2 = self.ReadLayer2(self.ports_in[0],self.tun_fd)        
        self.sch2.start()                
        while not self.finished :
            payload = os.read(self.tun_fd, 10*1024)
            if not payload:
                module_logger.debug(str(self.my_addr) +' an empty packet from the virtual ethernet interface ' )
            else:
                module_logger.debug(str(self.my_addr) +' Tx len(payload) : ' + str(len(payload)))
                event = if_events.mkevent("DataData")
                event.ev_dc['src_addr'] = self.my_addr
                event.ev_dc['dst_addr'] = self.dst_addr
                event.payload = payload
                try:
                    for q in self.ports_out[0]:
                        q.put(event, False)   # add to queue, don't block  
                        module_logger.debug(str(self.my_addr) +' L3: event from L3 transmited, queue size :  '+ str(q.qsize()) )
                except Queue.Full:
                    module_logger.debug(str(self.my_addr) +' Layer 3 to Layer 2 queue is full, packet loss   ' )

        return
    def stop(self):        
       self.finished = True
       self._Thread__stop()
       self.sch2.stop()
        
        
    class ReadLayer2(threading.Thread):
        '''Subclass of Scheduler for adapting layers 3 and 2.
        '''
        
        def __init__(self,in_queue,tun_fd):
            '''  
            Constructor
            
            @param mgmt_queue : The queue to put the management events.
            '''
            threading.Thread.__init__(self)
            self.in_queue = in_queue
            self.tun_fd = tun_fd
            self.finished = False
            self.logger = logging.getLogger(str(self.__class__))
            self.logger.debug('.... Layer 3 :creating an instance of Read layer 2 process')
            
            
        def run(self):
            '''Scheduling function, reads events, outputs events.
            
            Reads one element from the input event queue, and puts the event in the output queue.
            out_queues: a dictionary of {nm_queue: (out_queue)}; nm_queue is a name for the queue, out_queue is the output queue.
            '''
            while not self.finished :
                event = self.in_queue.get()
                payload = event.payload
                module_logger.debug(' Length of payload recieved from usrp  and send it to virtual interface: ' + str(len(payload)) )
                try:
                    os.write(self.tun_fd, payload)
                except:
                    print " OS payload error ", repr(payload)
            return
        def stop(self):
            self.finished = True
            self._Thread__stop()


def test():
    '''Tests the SchedLayer3 subclass.

    Puts some events in input queue, runs scheduler, puts events in output queue.
    '''



if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        sys.exit()

