#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Tue May  7 11:05:17 2013

@author: belza
'''

import sys
sys.path +=['..']
import libevents.if_events as if_events
import libgwnBlocks.gwnBlock as gwn


class EventSimulator(gwn.gwnBlock) :
    '''
    
    '''

    def __init__(self,nickname,param1=0,param2=0,param3=0):
        '''  
        Constructor.
        
        '''
        super(EventSimulator,self).__init__(1,1)        
        self.finished = False    
        self.nickname =nickname
        self.param1 = param1
        self.param2 =param2
        self.param3 = param3

       
        
    def run(self):
        while not self.finished :
            if self.nickname=="DataData":
                event = self.event_data()
            if self.nickname=="CtrlRTS":
                event = self.event_RTS()
            if self.nickname=="CtrlCTS":
                event = self.event_CTS()
            if self.nickname=="CtrlACK":
                event = self.event_ACK()
            if self.nickname=="TimerConfig":      
                event= self.event_timer_config()
            for q in self.ports_out[0]:
                q.put(event,False)
            "Wait for the next timer event to generate a new event"            
            event = self.ports_in[0].get()
    
    def stop(self):
        self.finished = True
        self._Thread__stop()

    def event_data(self):
        event = if_events.mkevent(self.nickname)
        event.ev_dc['src_addr'] = self.param1
        event.ev_dc['dst_addr'] = self.param2
        length= self.convert_int(self.param3)
        event.ev_dc['frame_length'] = length                         
        event.payload='1'*length
        return event            
    def event_RTS(self):
        event = if_events.mkevent(self.nickname)
        event.ev_dc['src_addr'] = self.param1
        event.ev_dc['dst_addr'] = self.param2
        return event        
    def event_CTS(self):
        event = if_events.mkevent(self.nickname)
        event.ev_dc['src_addr'] = self.param1
        event.ev_dc['dst_addr'] = self.param2
        return event
    def event_ACK(self):
        event = if_events.mkevent(self.nickname)
        event.ev_dc['src_addr'] = self.param1
        event.ev_dc['dst_addr'] = self.param2
        return event        
    def event_timer_config(self):
        event = if_events.mkevent(self.nickname)
        interval = self.convert_float(self.param1)
        event.ev_dc['interval']=interval
        retry=self.convert_int(self.param2)
        event.ev_dc['retry']=retry
        event.ev_dc['nickname1']= self.param3
        return event
    def convert_int(self,param):
        if isinstance(param,int):
            return(param)
        else:
            if isinstance(param,str):
                if param.isdigit():
                    return(int(param))

        return(0)
        
        
    def convert_float(self,param):
        if isinstance(param,float):
            return(param)
        else:
            if isinstance(param,str):
                try:
                    return(float(param))
                except ValueError:
                    return(0)
        return(0)