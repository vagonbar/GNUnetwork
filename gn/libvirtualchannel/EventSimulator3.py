#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Tue May  7 11:05:17 2013

@author: belza
'''

import sys,time
sys.path +=['..']
import libevents.if_events as if_events
import libgwnblocks.gwnblock as gwn


class EventSimulator(gwn.GWNBlock) :
    '''
    
    '''

    def __init__(self,interval,retry,nickname,param1=0,param2=0,param3=0):
        '''  
        Constructor.
        
        '''
        super(EventSimulator,self).__init__(1,"Simulator1",0,1,1)        
        self.finished = False    
        self.nickname =nickname
        self.param1 = param1
        self.param2 =param2
        self.param3 = param3
        self.interval = interval
        self.retry = retry
        self.set_timer(0,False,self.interval,self.retry)

       
        
    def process_data(self, port_type, port_nr, ev):
        if port_type == "intimer":
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
            self.write_out(0,event)
        else:
            pass
    
   
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
        

def test2():
    '''Test InPort, Block classses.
    '''
    blk1 = EventSimulator(2,5,"CtrlRTS",100,101)
    print blk1
    connector2 = gwn.AQueueConnector()
    #blk1.start()
    #time.sleep(2)

    blk1.set_connection_out(connector2,0)
    blk1.start()
    i=1    
    while i < 10:
        i=i+1    
        print connector2.get()
        
   
    time.sleep(10)
    blk1.stop()
    blk1.join()
    #blk1.stop()

 
    

if __name__ == '__main__':
    try:
        test2()
    except KeyboardInterrupt:
        pass

