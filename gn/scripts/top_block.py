#!/usr/bin/env python
##################################################
# GNU Wireless Network Flow Graph
# Title: Top Block
# Generated: Fri May 23 20:25:00 2014
##################################################
import os
os.chdir("/home/belza/Dropbox/gn/gn/scripts/")
print os.getcwd()

import sys
sys.path +=['..']
import libgwnBlocks.gwnTopBlock as gwnTB
import libtimer.timer2 as timer
import libvirtualchannel.EventConsumer2 as consumer
import libvirtualchannel.EventSimulator2 as simulator

class top_block(gwnTB.gwnTopBlock):


	def __init__(self, parametro1=12):
		gwnTB.gwnTopBlock.__init__(self)


		##################################################
		# Parameters
		##################################################
		self.parametro1 = parametro1

		##################################################
		# Variables
		##################################################
		self.variable_0 = variable_0 = 0.5

		##################################################
		# Blocks
		##################################################
		self.timer_1 = timer.Timer(5, 30,"TimerTOR2")	
		self.timer_0 = timer.Timer(variable_0, 2,"TimerTOR1")	
		self.eventsim_0 = simulator.EventSimulator('TimerConfig',"3","1","TimerTimer")	
		self.eventconsumer_1 = consumer.EventConsumer("nickname2") 	
		self.eventconsumer_0 = consumer.EventConsumer("nickname1") 	




		##################################################
		# Connections
		##################################################
		self.connect((self.timer_0, 0), (self.eventconsumer_0, 0))
		self.connect((self.eventsim_0, 0), (self.timer_0, 0))
		self.connect((self.timer_1, 0), (self.eventsim_0, 0))
		self.connect((self.timer_0, 0), (self.eventconsumer_1, 0))


		##################################################
		# Starting Bloks
		##################################################
		self.timer_1.start()
		self.timer_0.start()
		self.eventsim_0.start()
		self.eventconsumer_1.start()
		self.eventconsumer_0.start()


	def stop(self):

		##################################################
		# Ending Bloks
		##################################################
		self.timer_1.stop()
		self.timer_0.stop()
		self.eventsim_0.stop()
		self.eventconsumer_1.stop()
		self.eventconsumer_0.stop()



if __name__ == '__main__':
	tb = top_block()
	
	c = raw_input('Press #z to end, or #w to test commands :')        
    	while c != "#z":
       		c = raw_input('Press #z to end, or #w to test commands :')    

	    
	tb.stop()           
    	print "Program ends"
    	exit(0)

