#!/usr/bin/env python
##################################################
# GNU Wireless Network Flow Graph
# Title: Top Block
# Author: ARTES
# Generated: Thu Jul 10 14:10:26 2014
##################################################
import os
os.chdir("../../scripts/")
print os.getcwd()

import sys
sys.path +=['..']
import libgwnblocks.gwntopblock as gwnTB
import libtimer.timer2 as timer
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
		self.timer_0 = timer.Timer(1, 1, "TimerTimer")	
		self.eventsim_0 = simulator.EventSimulator(5,2, 'TimerConfig',"1","1","TimerTimer")	
		self.eventconsumer_0 = consumer.EventConsumer("blkname") 	




		##################################################
		# Connections
		##################################################
		self.connect((self.timer_0, 0), (self.eventconsumer_0, 0))
		self.connect((self.eventsim_0, 0), (self.timer_0, 0))


		##################################################
		# Starting Bloks
		##################################################
		self.timer_0.start()
		self.eventsim_0.start()
		self.eventconsumer_0.start()


	def stop(self):

		##################################################
		# Ending Bloks
		##################################################
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

