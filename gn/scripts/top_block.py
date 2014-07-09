#!/usr/bin/env python
##################################################
# GNU Wireless Network Flow Graph
# Title: Top Block
# Author: ARTES
# Generated: Wed Jul  9 12:41:57 2014
##################################################
import os
os.chdir("../../scripts/")
print os.getcwd()

import sys
sys.path +=['..']
import libgwnblocks.gwntopblock as gwnTB
import libgwnblocks.gwntuntap as tun_tap
import libvirtualchannel.eventconsumer2 as consumer
import libvirtualchannel.eventsimulator3 as simulator

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
		self.tun_tap_0 = tun_tap.TunTapInterface("/dev/net/tun","10:10:10:10:10:10","11:11:11:11:11:11")	
		self.eventsim_0 = simulator.EventSimulator(1,1, 'DataData',"1010101","101010","10")	
		self.eventconsumer_0 = consumer.EventConsumer("blkname") 	




		##################################################
		# Connections
		##################################################
		self.connect((self.eventsim_0, 0), (self.tun_tap_0, 0))
		self.connect((self.tun_tap_0, 0), (self.eventconsumer_0, 0))


		##################################################
		# Starting Bloks
		##################################################
		self.tun_tap_0.start()
		self.eventsim_0.start()
		self.eventconsumer_0.start()


	def stop(self):

		##################################################
		# Ending Bloks
		##################################################
		self.tun_tap_0.stop()
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

