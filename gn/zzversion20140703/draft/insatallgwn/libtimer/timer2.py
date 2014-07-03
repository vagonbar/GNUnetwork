#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Thu Dec 13 14:31:45 2012

@author: belza
'''
import sys
sys.path +=sys.path + ['..']
import time
import libevents.if_events as if_events
import libgwnBlocks.gwnBlock as gwn

class Timer(gwn.gwnBlock):
    '''A timerthat waits an interval and generates a Timer Event.
    This class is a timer that waits for a given interval. After that generates an event of Yype TIMER and Subtype the name given in subTypeEvent1.
    The timer retries the number of times gven in the parameter retry. After the given number of retries it generates the event of Type TIMER and subtype given in subTypeEvent2 if it is not None.
    '''

    def __init__(self, interval, retry,nickname1, \
            add_info=None, nickname2=None):
        '''  
        Constructor.
        
        @param interval: The interval of time.
        @param retry: The number of retries.
        @param nickname1: The nickname of the event that must be called after each retry.
        @param nickname2: The nickname of the event that must be called after the given number of retries.
        @param add_info: additional information that will be send with the Timer Event.
        '''        
        "The Timer has one output and 0 inputs so we must call the father constructor with parameters (0,1)"
        super(Timer,self).__init__(1,1)        
        self.interval = interval
        self.retry = retry
        self.nickname1=nickname1
        self.nickname2=nickname2
        self.add_info = add_info
        self.finished = False
        
    def run(self):
        '''This is the private thread that generates.
        '''
        i=1
        while not self.finished :       
            while i <= self.retry: 
                i=i+1
                time.sleep(self.interval)
                if self.finished:
                    return
                self.tout1()
            if self.nickname2 is not None:
                self.tout2()
            if self.ports_in[0]:                
                event = self.ports_in[0].get()
                if event.nickname == 'TimerConfig':
                    #print "Receive configuration event ",  event
                    self.set_config(event)
                    i=1
                else:
                    print " Receives the following event in the configuration port :", event
                    self.finished=True
            else :
                self.finished=True
    

    def tout1(self):      
            event= if_events.mkevent(self.nickname1)
            event.ev_dc['add_info'] =  self.add_info
            for q in self.ports_out[0]:
                q.put(event,False)


    def tout2(self):
            event= if_events.mkevent(self.nickname2)
            event.ev_dc['add_info'] =  self.add_info
            for q in self.ports_out[0]:
                q.put(event,False)
                
    def stop(self):
            self.finished = True
            self._Thread__stop()

    def set_config(self,event):
            if 'interval' in event.ev_dc:
                self.interval=event.ev_dc['interval']
            if 'retry' in event.ev_dc:
                self.retry = event.ev_dc['retry']
            if 'nickname1' in event.ev_dc:
                self.nickname1=event.ev_dc['nickname1']
            if 'nickname2' in event.ev_dc:
                self.nickname2=event.ev_dc['nickname2']
            else:
                self.nickname2=None
            if 'add_info' in event.ev_dc:
                self.add_info = event.ev_dc['add_info']
            else:
                self.add_info = None


