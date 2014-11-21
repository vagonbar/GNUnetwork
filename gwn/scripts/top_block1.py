#!/usr/bin/env python
##################################################
# GNU Wireless Network Flow Graph
# Title: Top Block1
# Generated: Wed Nov 19 11:39:58 2014
##################################################
import os
os.chdir("../../scripts/")
print os.getcwd()

import sys
sys.path +=['..']
import blocks.framers.ieee80211.deframer as deframer
import blocks.framers.ieee80211.framer as framer
import blocks.libio.gnuradio.new.gwnInterfaceTxRxqpsk as qpsk
import blocks.simulators.consumers.eventconsumer as consumer
import blocks.simulators.generators.eventsimulator as simulator
import gwnblocks.gwntopblock as gwnTB

class top_block1(gwnTB.GWNTopBlock):


	def __init__(self, queues_size=12):
		gwnTB.GWNTopBlock.__init__(self, queues_size=12)


		##################################################
		# Parameters
		##################################################
		self.queues_size = queues_size

		##################################################
		# Variables
		##################################################
		self.var_0 = var_0 = 1

		##################################################
		# Blocks
		##################################################
		self.psk_0 = qpsk.QPSK(2, 'TX/RX', 850000000.0, 15, "A:0", 15, "serial=E0R11Y4B1",  100000, 851000000.0, 0.25)	
		self.framer80211_0 = framer.Framer()	
		self.eventsim_0 = simulator.EventSimulator(1, 50, 'DataData', "aaaaaa", "bbbbb", "10")	
		self.eventconsumer_0 = consumer.EventConsumer("blkname") 	
		self.deframer80211_0 = deframer.Deframer()	




		##################################################
		# Connections
		##################################################
		self.connect((self.eventsim_0, 0), (self.framer80211_0, 0))
		self.connect((self.deframer80211_0, 0), (self.eventconsumer_0, 0))
		self.connect((self.framer80211_0, 0), (self.psk_0, 0))
		self.connect((self.psk_0, 0), (self.deframer80211_0, 0))


		##################################################
		# Starting Bloks
		##################################################
		self.psk_0.start()
		self.framer80211_0.start()
		self.eventsim_0.start()
		self.eventconsumer_0.start()
		self.deframer80211_0.start()


	def stop(self):

		##################################################
		# Ending Bloks
		##################################################
		self.psk_0.stop()
		self.framer80211_0.stop()
		self.eventsim_0.stop()
		self.eventconsumer_0.stop()
		self.deframer80211_0.stop()



if __name__ == '__main__':
	tb = top_block1()
	
	c = raw_input('Press #z to end, or #w to test commands :')        
    	while c != "#z":
       		c = raw_input('Press #z to end, or #w to test commands :')    

	    
	tb.stop()           
    	print "Program ends"
    	exit(0)

