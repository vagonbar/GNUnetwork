#!/usr/bin/env python
##################################################
# GNU Wireless Network Flow Graph
# Title: Top Block
# Generated: Fri May 16 10:44:54 2014
##################################################
import sys
sys.path +=['..']
import libgwnBlocks as gwn
import libtimer.timer2 as timer
import libvirtualchannel.EventConsumer2 as consumer

class top_block(gwn.TopBlock):


	def __init__(self, parametro1=12):
		gwnTopBlock.__init__(self)


		##################################################
		# Parameters
		##################################################
		self.parametro1 = parametro1

		##################################################
		# Variables
		##################################################
		self.variable_0 = variable_0 = 10

		##################################################
		# Blocks
		##################################################
		self.timer_0 = timer.Timer2(5, 4,"nickname1")	
		self.eventconsumer_0 = consumer.EventConsumer2("nickname1") 	




		##################################################
		# Connections
		##################################################
		self.connect((self.timer_0, 0), (self.eventconsumer_0, 0))


		##################################################
		# Starting Bloks
		##################################################
		self.timer_0.start()
		self.eventconsumer_0.start()


	def stop(self):

		##################################################
		# Ending Bloks
		##################################################
		self.timer_0.stop()
		self.eventconsumer_0.stop()



if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	tb = top_block()
	
	c = raw_input('Press #z to end, or #w to test commands :')        
    	while c != "#z":
       		c = raw_input('Press #z to end, or #w to test commands :')    

	    
	tb.stop()           
    	print "Program ends"
    	exit(0)

