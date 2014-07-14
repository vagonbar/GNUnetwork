#!/usr/bin/env python
##################################################
# GNU Wireless Network Flow Graph
# Title: Top Block
# Author: ARTES
# Generated: Mon Jul 14 20:47:04 2014
##################################################
import os
os.chdir("../../scripts/")
print os.getcwd()

import sys
sys.path +=['..']
import blocks.simulators.channels.virtualchannel as channel
import blocks.simulators.consumers.eventconsumer2 as consumer
import blocks.simulators.generators.eventsimulator3 as simulator
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
		self.virtualchannel_0 = channel.GWNVirtualChannel(0.01)	
		self.eventsim_0 = simulator.EventSimulator(1,3, 'TimerConfig',"","","")	
		self.eventconsumer_0 = consumer.EventConsumer("blkname") 	




		##################################################
		# Connections
		##################################################
		self.connect((self.eventsim_0, 0), (self.virtualchannel_0, 0))
		self.connect((self.virtualchannel_0, 0), (self.eventconsumer_0, 0))


		##################################################
		# Starting Bloks
		##################################################
		self.virtualchannel_0.start()
		self.eventsim_0.start()
		self.eventconsumer_0.start()


	def stop(self):

		##################################################
		# Ending Bloks
		##################################################
		self.virtualchannel_0.stop()
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

