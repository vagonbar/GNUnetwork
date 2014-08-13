#!/usr/bin/env python
##################################################
# GNU Wireless Network Flow Graph
# Title: Top Block
# Generated: Wed Aug 13 13:28:13 2014
##################################################
import os
os.chdir("../../scripts/")
print os.getcwd()

import sys
sys.path +=['..']
import blocks.simulators.consumers.eventconsumer as consumer
import blocks.simulators.generators.eventsimulator as simulator
import blocks.utilblocks.timer.timer as timer
import gwnblocks.gwntopblock as gwnTB

class top_block(gwnTB.GWNTopBlock):


	def __init__(self, parametro1=12):
		gwnTB.GWNTopBlock.__init__(self, parametro1=12)


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
		self.timer_0 = timer.Timer(variable_0, 2, "TimerTOR1")	
		self.eventsim_0 = simulator.EventSimulator(1, 1, 'TimerConfig', "3", "1", "TimerTimer")	
		self.eventconsumer_1 = consumer.EventConsumer("blkname") 	
		self.eventconsumer_0 = consumer.EventConsumer("blkname") 	




		##################################################
		# Connections
		##################################################
		self.connect((self.timer_0, 0), (self.eventconsumer_0, 0))
		self.connect((self.eventsim_0, 0), (self.timer_0, 0))
		self.connect((self.timer_0, 0), (self.eventconsumer_1, 0))


		##################################################
		# Starting Bloks
		##################################################
		self.timer_0.start()
		self.eventsim_0.start()
		self.eventconsumer_1.start()
		self.eventconsumer_0.start()


	def stop(self):

		##################################################
		# Ending Bloks
		##################################################
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

