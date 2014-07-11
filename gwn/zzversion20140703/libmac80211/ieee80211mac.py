# -*- coding: utf-8 -*-

"""
@author: ggomez
"""
import sys
sys.path +=['..']
import Queue,time,threading
import libfsm.fsm as fsm
import libevents.if_events as if_events
import libtimer.timer as Timer
import libmanagement.NetworkConfiguration as NetworkConfiguration
import libtimer.timer as Timer
import random
import libutils.gnlogger as gnlogger
import logging
module_logger = logging.getLogger(__name__)

Loses = 10
aSIFSTime = 1
aDIFSTime = 1
# "CTS_Time” shall be calculated using the length of the CTS frame and the data rate at which the RTS frame used for the most recent NAV update was received.
CTS_Time = 14*8/34000  # 14 bytes, 34M ??
aSlotTime = 1
aRTSThreshold = 60
aPHY_RX_START_Delay = 10
dot11LongRetryLimit = 5
dot11ShortRetryLimit = 5
CWmin = 15
CWmax = 1023
CTSTout = aSIFSTime + aSlotTime + aPHY_RX_START_Delay
ACKTout = aSIFSTime + aSlotTime + aPHY_RX_START_Delay

class ieee80211mac() :
    """   The 802.11 mac finite state machine.
	"""
	
    def __init__( self, nodeid, net_conf, timer_q, tx_ql1, tx_ql3 ):
		'''  
			Constructor
			@param tx_q: The transmition event queue ( Events to layer 1 )
        
		'''
		self.tx_ql1 = tx_ql1
		self.tx_ql3 = tx_ql3
		self.net_conf = net_conf
		self.nodeid = nodeid
		self.timer_q = timer_q
		
		self.LRC = 0 # Long Retry Counter
		self.SRC = 0 # Short Retry Counter
		self.NAV = 0 # Network Allocation Vector
		self.PAV = 0 # Physical Allocation Vector
		self.BC = 0 # Backoff
		self.CW = CWmin # Current Window
		self.logger = logging.getLogger( str( self.__class__ ) )
		self.datatosend = 0
	
		gnlogger.logconf()         # initializes the logging facility
		self.logger.info( str( self.nodeid )+ ' start' )

		self.mac_fsm = fsm.FSM ('IDLE', []) 
		self.mac_fsm.set_default_transition ( self.Error, 'IDLE')

		self.mac_fsm.add_transition      ('L3Data',		    'IDLE',            self.rcvL3,      'WAIT_ACK'	)
		self.mac_fsm.add_transition      ('Beacon',		    'IDLE',            self.rcvL3,      'WAIT_ACK'	)
		self.mac_fsm.add_transition      ('L1Data',			'IDLE',        	   self.rcvL1,      'IDLE'	 	)
		self.mac_fsm.add_transition      ('RTS',            'IDLE',        	   self.rcvRTS,     'IDLE'		)
		self.mac_fsm.add_transition      ('CTS',            'IDLE',        	   self.updNAV,     'IDLE'    	)
		self.mac_fsm.add_transition_any  (					'IDLE', 		   self.Error, 	   	'IDLE'    	)

		self.mac_fsm.add_transition      ('ACK',            'WAIT_ACK',        self.rcvACK, 	'IDLE'    	)
		self.mac_fsm.add_transition      ('ACKTout',     	'WAIT_ACK',        self.sndData,    'WAIT_ACK'	)
		self.mac_fsm.add_transition      ('DataAbort',     	'WAIT_ACK',        self.sndData,    'IDLE'		)
		self.mac_fsm.add_transition      ('RTS',            'WAIT_ACK',        self.rcvRTS,     'WAIT_CTS'	)
		self.mac_fsm.add_transition_any  (					'WAIT_ACK', 	   self.Error, 	   	'WAIT_ACK'	)

		self.mac_fsm.add_transition      ('CTS',            'WAIT_CTS',        self.sndData,    'WAIT_ACK'	)
		self.mac_fsm.add_transition      ('CTSTout', 	    'WAIT_CTS',        self.sndRTS,     'WAIT_CTS'	)
		self.mac_fsm.add_transition      ('RTSAbort', 	    'WAIT_CTS',        self.sndRTS,     'IDLE'		)
		self.mac_fsm.add_transition      ('RTS',            'WAIT_CTS',        self.rcvRTS,     'WAIT_CTS'	)
		self.mac_fsm.add_transition_any  (					'WAIT_CTS', 	   self.Error, 	   	'WAIT_CTS'	)

    def Error ( self, fsm ):
		self.logger.error( str( self.nodeid )+ ' Default transition for symbol: '+ str( fsm.input_symbol ) + ", state: " + str( fsm.current_state ) )
		return True

    def rcvL3( self, fsm ):
		self.logger.info( str( self.nodeid )+ ' Receive from L3' )
		event = self.mac_fsm.memory
		self.datatosend = self.mac_fsm.memory
		if ( event.ev_dc['frame_length'] > aRTSThreshold ):
			self.sndRTS( fsm )
			self.logger.debug( str( self.nodeid )+ ' start timer' )
			self.rtstimer=Timer.Timer( self.timer_q, CTSTout, dot11ShortRetryLimit, 'TimerCTSTout', None, 'TimerRTSAbort' )
			self.rtstimer.start()
			self.mac_fsm.next_state = 'WAIT_CTS'
		else:
			self.sndData( fsm )
			self.logger.debug( str( self.nodeid )+ ' start timer' )
			if ( self.datatosend.ev_dc['frame_length'] > aRTSThreshold ):
				self.datatimer=Timer.Timer( self.timer_q, ACKTout, dot11ShortRetryLimit, 'TimerACKTout', None, 'TimerDataAbort' )
			else:
				self.datatimer=Timer.Timer( self.timer_q, ACKTout, dot11LongRetryLimit, 'TimerACKTout', None, 'TimerDataAbort' )
			self.datatimer.start()
		return True

    def sndData ( self, fsm ):
		event = self.mac_fsm.memory
		if ( event.ev_subtype == 'ACKTout' ):
			if ( event.nickname == 'TimerDataAbort' ):
				self.logger.debug( str( self.nodeid )+ ' Send Data EXAUSTED' )
				self.discard()
				self.CW = CWmin
				self.SRC = 0
				self.LRC = 0
				self.datatimer.stop()
				return False
			elif ( event.nickname == 'TimerACKTout' ):
				self.logger.debug( str( self.nodeid )+ ' Send Data. Retry' )
				self.datatosend.ev_dc['retry'] = 1;
				if ( event.ev_dc['frame_length'] > aRTSThreshold ):
					self.LRC += 1
					if ( self.LRC >= dot11LongRetryLimit ):
						self.discard()
						self.datatimer.stop()
						self.CW = CWmin
						self.LRC = 0
						self.logger.debug( str( self.nodeid )+ ' LRC > ' + str( dot11LongRetryLimit ) )
						return False
				else:
					self.SRC += 1
					if ( self.SRC >= dot11ShortRetryLimit ):
						self.discard()
						self.CW = CWmin
						self.SRC = 0
						self.logger.debug( str( self.nodeid )+ ' SRC > ' + str( dot11ShortRetryLimit ) )
						return False
				self.snd_frame( self.datatosend )
		else:
			##self.snd_frame( self.mac_fsm.memory )
			self.snd_frame( self.datatosend )
		return True

    def snd_frame( self, event ):
		self.logger.info( str( self.nodeid )+ ' Send Frame' )
		txok = False;
		while ( txok == False ):
			self.logger.debug( str( self.nodeid )+ ' Loop LRC: ' + str(self.LRC) + ', SRC: ' + str( self.SRC) )
			#if ( self.SRC == 0 and self.LRC == 0 ):		# 1er intento
			#	self.backoff()
			if ( not ( event.ev_dc['frame_length'] > aRTSThreshold and self.LRC == 0 ) and not ( event.ev_dc['frame_length'] <= aRTSThreshold and self.SRC == 0 ) ):
#				# self.backoff()
#			else:
				self.CW = min( self.CW*2+1, CWmax )
				self.logger.debug( str( self.nodeid )+ ' Send Frame new CW ' + str( self.CW ) )
				self.backoff()
			if ( self.freeChannel() ):
				self.sendtoL1( event )
				self.logger.debug( str( self.nodeid )+ ' Send Frame (done)' )
				txok = True
				break;
			self.logger.debug( str( self.nodeid )+ ' Send Frame: keep waiting' )
		self.logger.debug( str( self.nodeid )+ ' Send Frame (done)' )
		return True
		
    def sndRTS ( self, fsm ):
		self.logger.info( str( self.nodeid )+ ' Send RTS' )
		rcv_event = self.mac_fsm.memory
		event = if_events.mkevent("CtrlRTS")
		event.ev_dc['src_addr']=self.net_conf.station_id
		event.ev_dc['dst_addr']= rcv_event.ev_dc['dst_addr']
		event.ev_dc['duration']=0;
		self.snd_frame( event )
		return True

    def sndCTS ( self, fsm ):
		self.logger.info( str( self.nodeid )+ ' Send CTS' )
		event = if_events.mkevent("CtrlCTS")
		event.ev_dc['src_addr']=self.net_conf.station_id
		rcv_event = self.mac_fsm.memory
		event.ev_dc['dst_addr']= rcv_event.ev_dc['src_addr']
		self.snd_frame( event )
		return True

    def rcvRTS ( self, fsm ):
		self.logger.info( str( self.nodeid )+ ' Receive RTS' )
		self.updNAV( fsm )
		event = self.mac_fsm.memory
		if ( event.ev_dc['dst_addr'] == self.net_conf.station_id ):
			self.logger.debug( str( self.nodeid )+ ' Receive RTS (for me)' )
			self.sndCTS( fsm )
		else:
			self.logger.debug( str( self.nodeid )+ ' Receive RTS (not for me, ignoring)' )
			self.mac_fsm.next_state = self.mac_fsm.current_state
		return True

    def updNAV ( self, fsm ):
		self.logger.info( str( self.nodeid )+ ' Update NAV' )
		event = self.mac_fsm.memory
		if ( fsm.input_symbol == "RTS" ):
			#waitT = 2*aSIFSTime + CTS_Time + 2*aSlotTime # tutorial
			waitT = 2*aSIFSTime + CTS_Time + aPHY_RX_START_Delay + 2*aSlotTime # norma
			time.sleep( waitT )
			self.NAV = self.currentTime()
		else:
			testNAV = self.currentTime() + int(event.ev_dc['duration'])
			if ( testNAV > self.NAV ):
				self.NAV = testNAV
		return True

    def sndACK ( self, fsm ):
		self.logger.info( str( self.nodeid )+ ' Send ACK' )
		event = if_events.mkevent("CtrlACK")
		event.ev_dc['src_addr']=self.net_conf.station_id
		rcv_event = self.mac_fsm.memory
		event.ev_dc['dst_addr']= rcv_event.ev_dc['src_addr']
		self.snd_frame( event )
		return True

    def rcvACK ( self, fsm ):
		self.logger.info( str( self.nodeid )+ ' Receive ACK' )
		event = self.mac_fsm.memory
		if ( event.ev_dc['dst_addr'] == self.net_conf.station_id ):
			self.logger.debug( str( self.nodeid )+ ' Receive ACK (for me)' )
			self.CW = CWmin
			if ( event.ev_dc['frame_length'] > aRTSThreshold ):
				self.LRC = 0
			else:
				self.SRC = 0
			self.datatimer.stop()
			## TODO fragmentation 
		else:
			self.logger.debug( str( self.nodeid )+ ' Receive ACK (not for me, ignoring)' )
			self.mac_fsm.next_state = self.mac_fsm.current_state
		return True

    def sendtoL1( self, event ):
		self.logger.info( str( self.nodeid )+ ' Transmit' )
		self.tx_ql1.put( event, False )
		return True
				
    def backoff( self ):
		self.logger.info( str( self.nodeid )+ ' Backoff BC: ' + str(self.BC) + ' CW: ' + str(self.CW) )
		if ( self.BC == 0 ):
			self.BC = random.randint( 0, self.CW )
			self.logger.debug( str( self.nodeid )+ ' Backoff new BC: ' + str(self.BC) )
		while ( self.BC != 0 ):
			time.sleep( aSlotTime )
			if ( max( self.NAV, self.PAV ) < ( self.currentTime() - aSlotTime ) ):
				while ( not self.freeChannel() ):
					self.waitfree()
				self.BC -= 1
				self.logger.debug( str( self.nodeid )+ ' Backoff new BC decrement: ' + str(self.BC) )
			else:
				while ( not self.freeChannel() ):
					self.waitfree()
				self.logger.debug( str( self.nodeid )+ ' Backoff sleep aDIFSTime' )
				time.sleep( aDIFSTime )
		return True

    def rcvL1 ( self, fsm ):
		self.logger.info( str( self.nodeid )+ ' Receive from L1' )
		self.updNAV( fsm )
		event = self.mac_fsm.memory
		if ( event.ev_dc['dst_addr'] == self.net_conf.station_id ):
			self.logger.debug( str( self.nodeid )+ ' Receive L1 data (for me)' )
			self.tx_ql3.put( event, False )
			time.sleep( aSIFSTime )
			self.sndACK( fsm )
		else:
			self.logger.debug( str( self.nodeid )+ ' Receive L1 data (not for me, ignoring)' )
			self.mac_fsm.next_state = self.mac_fsm.current_state
		return True

    def currentTime( self ):
		self.logger.debug( str( self.nodeid )+ ' Get current Time' )
		return time.time()

    def freeChannel( self ):
		self.logger.debug( str( self.nodeid )+ ' freeChannel?' )
		test = random.randint(0,100);
		if ( test > Loses ):
			self.logger.debug( str( self.nodeid )+ ' freeChannel: FREE' )
			return True
		else:
			self.logger.debug( str( self.nodeid )+ ' freeChannel: BUSY' )
			return False

    def waitfree( self ):
		self.logger.debug( str( self.nodeid )+ ' waitfree' )
		while ( not self.freeChannel() ):
			time.sleep( 1 )
		self.logger.debug( str( self.nodeid )+ ' waitfree, now free' )
		return True

    def discard( self ):
		self.logger.debug( str( self.nodeid )+ ' discard' )
		self.datatosend = 0
		self.mac_fsm.next_state = 'IDLE'
		return True

class ControllerMAC(threading.Thread) :
 
    def __init__(self, net_conf, rxq_l1_ctrl, rxq_l1_mgmt, rxq_l1_data, txq_l1, rxq_l3, txq_l3 ):
        threading.Thread.__init__(self)
        self.net_conf = net_conf
        self.rx_q_l1c = rxq_l1_ctrl
        self.rx_q_l1m = rxq_l1_mgmt
        self.rx_q_l1d = rxq_l1_data
        self.rx_q_l3 = rxq_l3
        self.tx_q_l1 = txq_l1
        self.tx_q_l3 = txq_l3
        self.finished = False
        self.mymac = None        
        self.nodeid = self.net_conf.station_id
        self.timer_q = Queue.Queue( 10 )
        self.logger = logging.getLogger( str( self.__class__ ) )
        gnlogger.logconf()         # initializes the logging facility

    def run(self):
        self.mymac = ieee80211mac( self.nodeid, self.net_conf, self.timer_q, self.tx_q_l1, self.tx_q_l3 )
        while not self.finished:
			# read timer events
			if ( not self.timer_q.empty() ):
				event = self.timer_q.get_nowait()
				self.logger.debug( str( self.nodeid )+ ' Timer event arrives at the fsm controller' )
				# print event, " ", int(round(time.time() * 1000))
				self.mymac.mac_fsm.memory = event
				self.mymac.mac_fsm.process( event.ev_subtype )
			# read control frames from L1
			if ( not self.rx_q_l1c.empty() ):
				event = self.rx_q_l1c.get_nowait()
				self.logger.debug( str( self.nodeid )+ ' L1 control event arrives at the fsm controller' )
				# print event, " ", int(round(time.time() * 1000))
				self.mymac.mac_fsm.memory = event
				self.mymac.mac_fsm.process( event.ev_subtype )
			# read data frames from L1
			if ( not self.rx_q_l1d.empty() ):
				event = self.rx_q_l1d.get_nowait()
				self.logger.debug( str( self.nodeid )+ ' L1 data event arrives at the fsm controller' )
				# print event, " ", int(round(time.time() * 1000)) 
				self.mymac.mac_fsm.memory = event
				self.mymac.mac_fsm.process( 'L1' + event.ev_subtype )
			if ( not self.rx_q_l3.empty() ):
				event = self.rx_q_l3.get_nowait()
				self.logger.debug( str( self.nodeid )+ ' L3 event arrives at the fsm controller' )
				# print event, " ", int(round(time.time() * 1000)) 
				self.mymac.mac_fsm.memory = event
				self.mymac.mac_fsm.process( 'L3' + event.ev_subtype )
			
    def stop(self):
        print "MAC: STOP Controller fsm emulator CALLED"
        self.finished = True
        print "MAC: Controller DONE"
        self._Thread__stop()

if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        pass
