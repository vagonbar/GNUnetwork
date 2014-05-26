#!/usr/bin/env python
##################################################
# GNU Wireless Network Flow Graph
# Title: Top Block1
# Generated: Mon May 26 13:26:57 2014
##################################################
import os
os.chdir("/home/belza/Desktop/Dropbox/gn/gn/scripts/")
print os.getcwd()

import sys
sys.path +=['..']
import libgwnBlocks.gwnTopBlock as gwnTB
import libtimer.timer2 as timer
import libutils.gwnEvtypeClassifier2 as classifier
import libvirtualchannel.EventConsumer2 as consumer
import libvirtualchannel.EventSimulator2 as simulator

class top_block1(gwnTB.gwnTopBlock):


	def __init__(self, queues_size=12):
		gwnTB.gwnTopBlock.__init__(self, queues_size=12)


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
		self.timer_1 = timer.Timer(5, 4,"TimerTOR2")	
		self.evtype_classifier_0 = classifier.EvtypeClassifier(5,["Data","Request","Ctrl","Mgmt","Timer"])	
		self.eventsim_0_0 = simulator.EventSimulator('TimerConfig',"1","10","TOH")	
		self.eventsim_0 = simulator.EventSimulator('DataData',"10:2:20:35","10:2:20:36","5")	
		self.eventconsumer_0 = consumer.EventConsumer("nickname1") 	




		##################################################
		# Connections
		##################################################
		self.connect((self.timer_1, 0), (self.eventsim_0, 0))
		self.connect((self.evtype_classifier_0, 0), (self.eventconsumer_0, 0))
		self.connect((self.timer_1, 0), (self.eventsim_0_0, 0))
		self.connect((self.eventsim_0_0, 0), (self.evtype_classifier_0, 0))
		self.connect((self.eventsim_0, 0), (self.evtype_classifier_0, 0))
		self.connect((self.evtype_classifier_0, 1), (self.eventconsumer_0, 0))


		##################################################
		# Starting Bloks
		##################################################
		self.timer_1.start()
		self.evtype_classifier_0.start()
		self.eventsim_0_0.start()
		self.eventsim_0.start()
		self.eventconsumer_0.start()


	def stop(self):

		##################################################
		# Ending Bloks
		##################################################
		self.timer_1.stop()
		self.evtype_classifier_0.stop()
		self.eventsim_0_0.stop()
		self.eventsim_0.stop()
		self.eventconsumer_0.stop()



if __name__ == '__main__':
	tb = top_block1()
	
	c = raw_input('Press #z to end, or #w to test commands :')        
    	while c != "#z":
       		c = raw_input('Press #z to end, or #w to test commands :')    

	    
	tb.stop()           
    	print "Program ends"
    	exit(0)

