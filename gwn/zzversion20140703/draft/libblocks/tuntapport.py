#!/usr/bin/env python
# -*- coding: utf-8 -*-


import fcntl
import os
import struct
import subprocess

import Queue
import time
import sys

import gwninport
import gwnblock





class ATunTapConnector(gwninport.Connector):
    '''A Connector with a TUN/TAP interface.
    '''


    def __init__(self, maxsize=15):
        self.lsevents = Queue.Queue(maxsize=maxsize)

        # constants used to ioctl the device file
        TUNSETIFF = 0x400454ca
        TUNSETOWNER = TUNSETIFF + 2
        IFF_TUN = 0x0001
        IFF_TAP = 0x0002
        IFF_NO_PI = 0x1000

        # Open TUN device file.
        self.tun = open('/dev/net/tun', 'r+b')
        # Tall it we want a TUN device named tun0.
        ifr = struct.pack('16sH', 'tun0', IFF_TUN | IFF_NO_PI)
        fcntl.ioctl(self.tun, TUNSETIFF, ifr)
        # Optionally, we want it be accessed by the normal user.
        fcntl.ioctl(self.tun, TUNSETOWNER, 1000)

        # Bring it up and assign addresses.
        #    receives in 192.168.7.2
        #subprocess.check_call('ifconfig tun0 192.168.7.1 pointopoint 192.168.7.2 up', \
        #    shell=True)
        subprocess.check_call('ifconfig tun0 192.168.7.1 up', \
            shell=True)

    def get(self):
        packet = list(os.read(self.tun.fileno(), 2048))
        if packet:
            return packet
        else:
            return None
        """
        try:
            ev = self.lsevents.get(True, 1)
        except Queue.Empty:
            ev = None
        return ev
        """

    def put(self, ev):
        try:
            self.lsevents.put(ev, True, 1)
        except Queue.Full:
            print 'QueueConnector full, event %s discarded' % (ev,)
        return



### testing section


def test1():
    '''Tests ATunTapConnector class.
    '''
    conn = ATunTapConnector()
    print conn.lsevents
    for i in range(0,3):
        print conn.get(),
    print
    """for i in range(0,3):
        conn.put('A' + str(i))
    print conn.lsevents
    while not conn.is_empty():
        print conn.get(),
    print"""


class TunTapBlock(gwnblock.GWNBlock):
    '''A TUN/TAP block.
    '''
    def process_data(self, port_type, port_nr, ev):
        """print 'Received, block %s, port %d, event %s... ' % \
            (self.blkname, port_nr, ev),"""
        #self.write_out(0, ev)
        print "TUN/TAP, received", ev
        #print 'done.'
        return

def test2():
    blk2 = TunTapBlock(1, 'BlkTunTapReceive', 1, 0)
    conn1 = ATunTapConnector()
    blk2.set_connection_in(conn1, 0)

    blk2.start()
    time.sleep(10)

    blk2.stop()
    blk2.join()





if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '2':
            test = test2
        elif sys.argv[1] == '3':
            test = test3
        elif sys.argv[1] == '4':
            test = test4
    else:
        test = test2
        print 'tuntapport: please do'
        print '   python tuntapport.py <number of test to run: 2, 3 or 4> '

    try:
        test()
    except KeyboardInterrupt:
        pass