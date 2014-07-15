#!/usr/bin/env python
##################################################
# GNU Wireless Network Flow Graph
# Title: Top Block
# Author: ARTES
# Generated: Tue Jul 15 16:47:35 2014
##################################################
import os
os.chdir("../../scripts/")
print os.getcwd()

import sys
sys.path +=['..']
import blocks.libio.libadaptlay80211.deframer as deframer
import blocks.libio.libadaptlay80211.framer as framer
import blocks.mac.generic_fdma.genericfdma as fdma
import blocks.simulators.channels.virtualchannel as channel
import blocks.simulators.consumers.eventconsumer as consumer
import blocks.simulators.generators.eventsimulator as simulator
import gwnblocks.gwntopblock as gwnTB

class top_block(gwnTB.GWNTopBlock):


	def __init__(self):
		gwnTB.GWNTopBlock.__init__(self)


		##################################################
		# Blocks
		##################################################
		self.virtualchannel_1 = channel.GWNVirtualChannel(0.01)	
		self.virtualchannel_0 = channel.GWNVirtualChannel(1)	
		self.genericfdma_0_0 = fdma.GenericFDMA(851000000.0,850000000.0)	
		self.genericfdma_0 = fdma.GenericFDMA(851000000.0,850000000.0)	
		self.framer80211_0_0 = framer.Framer()	
		self.framer80211_0 = framer.Framer()	
		self.eventsim_0_0 = simulator.EventSimulator(1, 10, 'DataData', "101", "100", "10")	
		self.eventsim_0 = simulator.EventSimulator(1, 10, 'DataData', "100", "101", "10")	
		self.eventconsumer_0_0 = consumer.EventConsumer("blkname") 	
		self.eventconsumer_0 = consumer.EventConsumer("blkname") 	
		self.deframer80211_0_0 = deframer.Deframer()	
		self.deframer80211_0 = deframer.Deframer()	




		##################################################
		# Connections
		##################################################
		self.connect((self.deframer80211_0, 0), (self.genericfdma_0, 1))
		self.connect((self.virtualchannel_0, 0), (self.deframer80211_0, 0))
		self.connect((self.genericfdma_0, 0), (self.framer80211_0, 0))
		self.connect((self.eventsim_0, 0), (self.genericfdma_0, 0))
		self.connect((self.genericfdma_0, 1), (self.eventconsumer_0, 0))
		self.connect((self.deframer80211_0_0, 0), (self.genericfdma_0_0, 1))
		self.connect((self.genericfdma_0_0, 0), (self.framer80211_0_0, 0))
		self.connect((self.eventsim_0_0, 0), (self.genericfdma_0_0, 0))
		self.connect((self.genericfdma_0_0, 1), (self.eventconsumer_0_0, 0))
		self.connect((self.framer80211_0_0, 0), (self.virtualchannel_0, 0))
		self.connect((self.framer80211_0, 0), (self.virtualchannel_1, 0))
		self.connect((self.virtualchannel_1, 0), (self.deframer80211_0_0, 0))


		##################################################
		# Starting Bloks
		##################################################
		self.virtualchannel_1.start()
		self.virtualchannel_0.start()
		self.genericfdma_0_0.start()
		self.genericfdma_0.start()
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
		self.virtualchannel_1.stop()
		self.virtualchannel_0.stop()
		self.genericfdma_0_0.stop()
		self.genericfdma_0.stop()
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

