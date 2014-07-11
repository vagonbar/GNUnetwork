#!/usr/bin/env python
##################################################
# GNU Wireless Network Flow Graph
# Title: Top Block
# Author: ARTES
# Generated: Thu Jun  5 18:12:00 2014
##################################################
import os
os.chdir("../../scripts/")
print os.getcwd()

import sys
sys.path +=['..']
import libMAC.gwnSimpleFDMA as fdma
import libadaptlay80211.gwnDeframer as deframer
import libadaptlay80211.gwnFramer as framer
import libgwnBlocks.gwnTopBlock as gwnTB
import libtimer.timer2 as timer
import libvirtualchannel.EventConsumer2 as consumer
import libvirtualchannel.EventSimulator2 as simulator
import libvirtualchannel.gwnVirtualChannel as channel

class top_block(gwnTB.gwnTopBlock):


	def __init__(self):
		gwnTB.gwnTopBlock.__init__(self)


		##################################################
		# Blocks
		##################################################
		self.virtualchannel_0 = channel.gwnVirtualChannel(0.01)	
		self.timer_0_0 = timer.Timer(7, 3,"TimerTimer")	
		self.timer_0 = timer.Timer(5, 3,"TimerTimer")	
		self.simplefdma_0_0 = fdma.gwnSimpleFDMA(851000000.0,850000000.0)	
		self.simplefdma_0 = fdma.gwnSimpleFDMA(851000000.0,850000000.0)	
		self.framer80211_0_0 = framer.gwnFramer()	
		self.framer80211_0 = framer.gwnFramer()	
		self.eventsim_0_0 = simulator.EventSimulator('DataData',"101","100","10")	
		self.eventsim_0 = simulator.EventSimulator('DataData',"100","101","10")	
		self.eventconsumer_0_0 = consumer.EventConsumer("Consumer Node 2") 	
		self.eventconsumer_0 = consumer.EventConsumer("Consumer Node 1") 	
		self.deframer80211_0_0 = deframer.gwnDeframer()	
		self.deframer80211_0 = deframer.gwnDeframer()	




		##################################################
		# Connections
		##################################################
		self.connect((self.deframer80211_0, 0), (self.simplefdma_0, 1))
		self.connect((self.virtualchannel_0, 0), (self.deframer80211_0, 0))
		self.connect((self.framer80211_0, 0), (self.virtualchannel_0, 0))
		self.connect((self.simplefdma_0, 0), (self.framer80211_0, 0))
		self.connect((self.timer_0, 0), (self.eventsim_0, 0))
		self.connect((self.eventsim_0, 0), (self.simplefdma_0, 0))
		self.connect((self.simplefdma_0, 1), (self.eventconsumer_0, 0))
		self.connect((self.deframer80211_0_0, 0), (self.simplefdma_0_0, 1))
		self.connect((self.simplefdma_0_0, 0), (self.framer80211_0_0, 0))
		self.connect((self.timer_0_0, 0), (self.eventsim_0_0, 0))
		self.connect((self.eventsim_0_0, 0), (self.simplefdma_0_0, 0))
		self.connect((self.simplefdma_0_0, 1), (self.eventconsumer_0_0, 0))
		self.connect((self.framer80211_0_0, 0), (self.virtualchannel_0, 0))
		self.connect((self.virtualchannel_0, 0), (self.deframer80211_0_0, 0))


		##################################################
		# Starting Bloks
		##################################################
		self.virtualchannel_0.start()
		self.timer_0_0.start()
		self.timer_0.start()
		self.simplefdma_0_0.start()
		self.simplefdma_0.start()
		self.framer80211_0_0.start()
		self.framer80211_0.start()
		self.eventsim_0_0.start()
		self.eventsim_0.start()
		self.eventconsumer_0_0.start()
		self.eventconsumer_0.start()
		self.deframer80211_0_0.start()
		self.deframer80211_0.start()


	def stop(self):

		##################################################
		# Ending Bloks
		##################################################
		self.virtualchannel_0.stop()
		self.timer_0_0.stop()
		self.timer_0.stop()
		self.simplefdma_0_0.stop()
		self.simplefdma_0.stop()
		self.framer80211_0_0.stop()
		self.framer80211_0.stop()
		self.eventsim_0_0.stop()
		self.eventsim_0.stop()
		self.eventconsumer_0_0.stop()
		self.eventconsumer_0.stop()
		self.deframer80211_0_0.stop()
		self.deframer80211_0.stop()



if __name__ == '__main__':
	tb = top_block()
	
	c = raw_input('Press #z to end, or #w to test commands :')        
    	while c != "#z":
       		c = raw_input('Press #z to end, or #w to test commands :')    

	    
	tb.stop()           
    	print "Program ends"
    	exit(0)

