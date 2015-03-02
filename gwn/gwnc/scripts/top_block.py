#!/usr/bin/env python
##################################################
# GNU Wireless Network Flow Graph
# Title: Top Block
# Author: ARTES
# Generated: Mon Mar  2 14:15:58 2015
##################################################
import os
os.chdir("../../scripts/")
print os.getcwd()

import sys
sys.path +=['..']
import blocks.framers.ieee80211.deframer as deframer
import blocks.framers.ieee80211.framer as framer
import blocks.simulators.channels.virtualchannel as channel
import blocks.simulators.consumers.eventconsumer as consumer
import blocks.simulators.generators.eventsimulator as simulator
import gwnblocks.gwntopblock as gwnTB
import libutils.gwnEvtypeClassifier2 as classifier

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
		self.virtualchannel_0 = channel.GWNVirtualChannel(0.5)	
		self.framer80211_0 = framer.Framer()	
		self.evtype_classifier_0 = classifier.EvtypeClassifier(5,["Data","Ctrl","Timer","Timer","Timer"])	
		self.eventsim_0_0 = simulator.EventSimulator(1.0, 10, 'CtrlRTS', "100", "101", "10")	
		self.eventsim_0 = simulator.EventSimulator(1.0, 10, 'DataData', "100", "101", "10")	
		self.eventconsumer_0_1 = consumer.EventConsumer("Cons Ctrl") 	
		self.eventconsumer_0_0 = consumer.EventConsumer("Cons Data") 	
		self.eventconsumer_0 = consumer.EventConsumer("blkname") 	
		self.deframer80211_0 = deframer.Deframer()	




		##################################################
		# Connections
		##################################################
		self.connect((self.virtualchannel_0, 0), (self.deframer80211_0, 0))
		self.connect((self.framer80211_0, 0), (self.virtualchannel_0, 0))
		self.connect((self.eventsim_0, 0), (self.framer80211_0, 0))
		self.connect((self.eventsim_0_0, 0), (self.framer80211_0, 0))
		self.connect((self.deframer80211_0, 0), (self.eventconsumer_0, 0))
		self.connect((self.deframer80211_0, 0), (self.evtype_classifier_0, 0))
		self.connect((self.evtype_classifier_0, 0), (self.eventconsumer_0_0, 0))
		self.connect((self.evtype_classifier_0, 1), (self.eventconsumer_0_1, 0))


		##################################################
		# Starting Bloks
		##################################################
		self.virtualchannel_0.start()
		self.framer80211_0.start()
		self.evtype_classifier_0.start()
		self.eventsim_0_0.start()
		self.eventsim_0.start()
		self.eventconsumer_0_1.start()
		self.eventconsumer_0_0.start()
		self.eventconsumer_0.start()
		self.deframer80211_0.start()


	def stop(self):

		##################################################
		# Ending Bloks
		##################################################
		self.virtualchannel_0.stop()
		self.framer80211_0.stop()
		self.evtype_classifier_0.stop()
		self.eventsim_0_0.stop()
		self.eventsim_0.stop()
		self.eventconsumer_0_1.stop()
		self.eventconsumer_0_0.stop()
		self.eventconsumer_0.stop()
		self.deframer80211_0.stop()



if __name__ == '__main__':
	tb = top_block()
	
	c = raw_input('Press #z to end, or #w to test commands :')        
    	while c != "#z":
       		c = raw_input('Press #z to end, or #w to test commands :')    

	    
	tb.stop()           
    	print "Program ends"
    	exit(0)

