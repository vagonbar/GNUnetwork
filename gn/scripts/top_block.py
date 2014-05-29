#!/usr/bin/env python
##################################################
# GNU Wireless Network Flow Graph
# Title: Top Block
# Author: ARTES
# Generated: Thu May 29 13:54:28 2014
##################################################
import os
os.chdir("../../scripts/")
print os.getcwd()

import sys
sys.path +=['..']
import libadaptationlayer.TunTapInterface as tun_tap
import libgwnBlocks.gwnTopBlock as gwnTB
import libtimer.timer2 as timer
import libvirtualchannel.EventConsumer2 as consumer
import libvirtualchannel.EventSimulator2 as simulator

class top_block(gwnTB.gwnTopBlock):


	def __init__(self):
		gwnTB.gwnTopBlock.__init__(self)


		##################################################
		# Variables
		##################################################
		self.samp_rate = samp_rate = 32000

		##################################################
		# Blocks
		##################################################
		self.tun_tap_0 = tun_tap.TunTapInterface("/dev/net/tun","10:10:10:10:10:10","11:11:11:11:11:11")	
		self.timer_0 = timer.Timer(1000, 0,"Timer")	
		self.eventsim_0 = simulator.EventSimulator('DataData',"1010101","101010","10")	
		self.eventconsumer_0 = consumer.EventConsumer("nickname1") 	




		##################################################
		# Connections
		##################################################
		self.connect((self.timer_0, 0), (self.eventsim_0, 0))
		self.connect((self.eventsim_0, 0), (self.tun_tap_0, 0))
		self.connect((self.tun_tap_0, 0), (self.eventconsumer_0, 0))


		##################################################
		# Starting Bloks
		##################################################
		self.tun_tap_0.start()
		self.timer_0.start()
		self.eventsim_0.start()
		self.eventconsumer_0.start()


	def stop(self):

		##################################################
		# Ending Bloks
		##################################################
		self.tun_tap_0.stop()
		self.timer_0.stop()
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

