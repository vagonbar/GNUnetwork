#!/usr/bin/env python
##################################################
# GNU Wireless Network Flow Graph
# Title: Top Block1
# Generated: Tue Jun  3 17:40:38 2014
##################################################
import os
os.chdir("../../scripts/")
print os.getcwd()

import sys
sys.path +=['..']
import libMAC.gwnSimpleFDMA as fdma
import libadaptlay80211.gwnDeframer as deframer
import libadaptlay80211.gwnFramer as framer
import libgnuradio.gwnGnuRadiopsk as psk
import libgwnBlocks.gwnTopBlock as gwnTB
import libtimer.timer2 as timer
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
		self.timer_0 = timer.Timer(1, 300,"TimerTimer")	
		self.simplefdma_0 = fdma.gwnSimpleFDMA(851000000.0,850000000.0)	
		self.gnuradio_psk_0 = psk.gwnGnuRadiopsk( 2, "6", 'TX/RX', 850000000.0, 15, "A:0", 15, 'bpsk', "serial=E0R11Y0B1",  100000, 851000000.0, 0.25)	
		self.framer80211_0 = framer.gwnFramer()	
		self.eventsim_0 = simulator.EventSimulator('DataData',"10:10:10:10:10:10","10:10:10:10:10:11","10")	
		self.eventconsumer_0 = consumer.EventConsumer("nickname1") 	
		self.deframer80211_0 = deframer.gwnDeframer()	




		##################################################
		# Connections
		##################################################
		self.connect((self.simplefdma_0, 0), (self.framer80211_0, 0))
		self.connect((self.framer80211_0, 0), (self.gnuradio_psk_0, 0))
		self.connect((self.gnuradio_psk_0, 0), (self.deframer80211_0, 0))
		self.connect((self.deframer80211_0, 0), (self.simplefdma_0, 1))
		self.connect((self.timer_0, 0), (self.eventsim_0, 0))
		self.connect((self.eventsim_0, 0), (self.simplefdma_0, 0))
		self.connect((self.simplefdma_0, 1), (self.eventconsumer_0, 0))


		##################################################
		# Starting Bloks
		##################################################
		self.timer_0.start()
		self.simplefdma_0.start()
		self.gnuradio_psk_0.start()
		self.framer80211_0.start()
		self.eventsim_0.start()
		self.eventconsumer_0.start()
		self.deframer80211_0.start()


	def stop(self):

		##################################################
		# Ending Bloks
		##################################################
		self.timer_0.stop()
		self.simplefdma_0.stop()
		self.gnuradio_psk_0.stop()
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

