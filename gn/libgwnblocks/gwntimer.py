#!/usr/bin/env python
# -*- coding: utf-8 -*-


import gwnblock
from gwnblock import thread_lock

import threading
import time
import libevents.if_events as if_events

class InTimer(threading.Thread):
    '''Generates timing events.
    '''
    def __init__(self, block, port_nr, interval=1,retry=1,nickname1="TimerTimer",nickname2=None,add_info=None):
        '''Constructor.

        @param block: the block to which this instance is attached.
        @param port_nr: the "port number" assigned to this instance; it it an index in the list of timers in the container block.
        @param interval: time between events.
        '''
        threading.Thread.__init__(self)
        self.accept = []
        self.block = block
        self.port_nr = ("intimer",port_nr)
        self.exit_flag = False
        self.interrupt = True

        self.interval = interval
        self.retry = retry
        self.nickname1 = nickname1
        self.nickname2 = nickname2 
        self.add_info = add_info
        self.counter = 0


    def set_interrupt(self, interrupt):
        '''Interrupts generation of timer events.
        '''
        self.interrupt = interrupt


    def run(self):
        '''Runs thread, generates events regularly.

        TODO: uses time.sleep(), cannot resume execution until this function finishes.'''
        print '  Starting InTimer %d in block %s' % \
            (self.port_nr[1], self.block.blkname)
        while not self.exit_flag:
            if not self.interrupt:
                i=1
                while i <= self.retry: 
                    i=i+1
                    time.sleep(self.interval)
                    if not self.interrupt:
                        self.tout1()
                    else:
                        break    
                if not self.interrupt:
                    if self.nickname2 is not None:
                        self.tout2()
                self.interrupt=True
            else:
                time.sleep(0.01)
        return


    def tout1(self):      
        ev = if_events.mkevent(self.nickname1)
        ev.ev_dc['add_info'] = self.add_info
        thread_lock.acquire()
        #print '    port %d in block %s generated event %s' % \
        #    (self.port_nr, self.block.blkname, ev)
        print '   %s' % (ev,)
        self.block.process_data(self.port_nr, ev)
        thread_lock.release()
     

    def tout2(self):
        ev= if_events.mkevent(self.nickname2)
        ev.ev_dc['add_info'] =  self.add_info
        thread_lock.acquire()
        #print '    port %d in block %s generated event %s' % \
        #    (self.port_nr, self.block.blkname, ev)
        print '   %s' % (ev,)
        self.block.process_data(self.port_nr, ev)
        thread_lock.release()


    def stop(self):
        '''Stops thread.'''
        print '  ...stopping timer %d in block %s' % (self.port_nr[1], self.block.blkname)
        self.exit_flag = True
        return


    def __str__(self):
        ssaccept = ''
        for ev in self.accept:
            ssaccept += ev + ' '
        #return '%s: accepted events: %s, connector empty: %s' % \
        #     (self.__class__, ssaccept, self.conn.is_empty() )
        #return  '  timer [port] %d in block %s, thread %d' % \
        #    (self.port_nr, self.block.blkname, self.get_ident())
        return  '  timer [port] %d in block %s' % \
            (self.port_nr[1], self.block.blkname)


def test():
    '''Test InTimer.
    '''

    # create timers
    timer0 = InTimer(None, 0, 1)
    #print timer0
    #blk1.ports_in[0] = timer0
    timer1 = InTimer(None, 1, 2)
    #print timer1
    #blk1.ports_in[1] = timer1

    blk1 = gwnblock.GWNBlock(1, 'BlockTimer', 0, 0, [])
    timer0.block, timer0.port_nr = blk1, 0
    timer1.block, timer1.port_nr = blk1, 1
    blk1.set_timers([timer0, timer1])
    print blk1

    blk1.start()

    time.sleep(5)

    print '--- stopping timer 1 ---'
    blk1.timers[1].set_interrupt(True)
    time.sleep(5)
    print '--- restarting timer 1 ---'
    blk1.timers[1].set_interrupt(False)
    time.sleep(5)

    blk1.stop()
    blk1.join()
    #blk1.stop()


if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        pass
