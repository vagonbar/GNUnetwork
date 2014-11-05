#!/usr/bin/env python
##################################################
# GNU Wireless Network Flow Graph
# Title: Top Block
# Author: ARTES
# Generated: Mon Nov  3 10:40:44 2014
##################################################
import os
os.chdir("../../scripts/")
print os.getcwd()

import sys
sys.path +=['..']
import blocks.framers.ieee80211.deframer as deframer
import blocks.framers.ieee80211.framer as framer
import blocks.libio.gnuradio.new.gwnChannelqpsk as psk
import blocks.simulators.consumers.eventconsumer as consumer
import blocks.simulators.generators.eventsimulator as simulator
import gwnblocks.gwntopblock as gwnTB

class top_block(gwnTB.GWNTopBlock):


	def __init__(self):
		gwnTB.GWNTopBlock.__init__(self)


		##################################################
		# Variables
		##################################################
		self.samp_rate = samp_rate = 32000

		##################################################
		# Blocks
		##################################################
		self.qpsk_channel_0_0 = psk.ChannelQPSK(0.01,0.001,1.001,(1.0 + 0.5j, ))	
		self.qpsk_channel_0 = psk.ChannelQPSK(0.01,0.001,1.001,(1.0 + 0.5j, ))	
		self.framer80211_0 = framer.Framer()	
		self.eventsim_0 = simulator.EventSimulator(1, 4, 'DataData', "aaaaaa", "bbbbbb", "10")	
		self.eventconsumer_0_0 = consumer.EventConsumer("Number 2") 	
		self.deframer80211_0_0 = deframer.Deframer()	




		##################################################
		# Connections
		##################################################
		self.connect((self.eventsim_0, 0), (self.framer80211_0, 0))
		self.connect((self.framer80211_0, 0), (self.qpsk_channel_0, 0))
		self.connect((self.qpsk_channel_0_0, 0), (self.deframer80211_0_0, 0))
		self.connect((self.deframer80211_0_0, 0), (self.eventconsumer_0_0, 0))
		self.connect((self.qpsk_channel_0, 0), (self.qpsk_channel_0_0, 0))


		##################################################
		# Starting Bloks
		##################################################
		self.qpsk_channel_0_0.start()
		self.qpsk_channel_0.start()
		self.framer80211_0.start()
		self.eventsim_0.start()
		self.eventconsumer_0_0.start()
		self.deframer80211_0_0.start()


	def stop(self):

		##################################################
		# Ending Bloks
		##################################################
		self.qpsk_channel_0_0.stop()
		self.qpsk_channel_0.stop()
		self.framer80211_0.stop()
		self.eventsim_0.stop()
		self.eventconsumer_0_0.stop()
		self.deframer80211_0_0.stop()



if __name__ == '__main__':
	tb = top_block()
	
	c = raw_input('Press #z to end, or #w to test commands :')        
    	while c != "#z":
       		c = raw_input('Press #z to end, or #w to test commands :')    

	    
	tb.stop()           
    	print "Program ends"
    	exit(0)

