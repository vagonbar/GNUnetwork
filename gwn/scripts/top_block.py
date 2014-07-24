#!/usr/bin/env python
##################################################
# GNU Wireless Network Flow Graph
# Title: Top Block
# Author: ARTES
# Generated: Thu Jul 24 16:22:50 2014
##################################################
import os
os.chdir("../../scripts/")
print os.getcwd()

import sys
sys.path +=['..']
import blocks.framers.ieee80211.framer as framer
import blocks.libio.gnuradio.psk as psk
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
		self.psk_0 = psk.PSK(2, "6", 'TX/RX', 850000000.0, 15, "A:0", 15, 'bpsk', "serial=E0R11Y0B1",  100000, 851000000.0, 0.25)	
		self.framer80211_0 = framer.Framer()	
		self.eventsim_0 = simulator.EventSimulator(1, 3, 'DataData', "0001", "0002", "10")	
		self.eventconsumer_0 = consumer.EventConsumer("blkname") 	




		##################################################
		# Connections
		##################################################
		self.connect((self.eventsim_0, 0), (self.framer80211_0, 0))
		self.connect((self.framer80211_0, 0), (self.psk_0, 0))
		self.connect((self.psk_0, 0), (self.eventconsumer_0, 0))


		##################################################
		# Starting Bloks
		##################################################
		self.psk_0.start()
		self.framer80211_0.start()
		self.eventsim_0.start()
		self.eventconsumer_0.start()


	def stop(self):

		##################################################
		# Ending Bloks
		##################################################
		self.psk_0.stop()
		self.framer80211_0.stop()
		self.eventsim_0.stop()
		self.eventconsumer_0.stop()



if __name__ == '__main__':
	tb = top_block()
	
	c = raw_input('Press #z to end, or #w to test commands :')        
    	while c != "#z":
       		c = raw_input('Press #z to end, or #w to test commands :')    

	    
	tb.stop()           
    	print "Program ends"
    	exit(0)

