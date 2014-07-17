#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Thu Dec 13 14:31:45 2012

@author: belza
'''

import sys
sys.path +=['..']

# From gr-digital
from gnuradio import digital
import Queue
import threading
import libevents.if_events as if_events
import TxRxLayer1 as TxRxLayer1
import libgwnBlocks.gwnBlock as gwn

        

# /////////////////////////////////////////////////////////////////////////////
#                                   main
# /////////////////////////////////////////////////////////////////////////////


class GWNGnuRadioPSK(gwn.gwnBlock):

    def __init__(self,  samples_per_symbol= 2, version= '6', antenna= 'TX/RX', rx_freq= 850000000.0, rx_gain= 15.0, spec= 'A:0', tx_gain= 15.0, modulation= 'bpsk', args= 'serial=E0R11Y0B1',  bitrate= 100000.0, tx_freq= 851000000.0,  tx_amplitude= 0.25):
        super(GWNGnuRadioPSK,self).__init__(1,1)
        self.mods = digital.modulation_utils.type_1_mods()
        self.demods = digital.modulation_utils.type_1_demods()
        opt = {'verbose': True,  'samples_per_symbol': 2, 'chbw_factor': 1.0,  'log': False,  'version': '6', 'antenna': 'TX/RX', 'rx_freq': 850000000.0, 'version': '6',  'rx_gain': 15.0, 'spec': 'A:0', 'tx_gain': 15.0, 'modulation': 'bpsk', 'args': 'serial=E0R11Y0B1',  'freq': None, 'bitrate': 100000.0,  'from_file': None, 'to_file': None,  'tx_freq': 851000000.0, 'tx_amplitude': 0.25}        
        #self.mods = {'psk': <class 'gnuradio.digital.psk.psk_mod'>, 'cpm': <class 'gnuradio.digital.cpm.cpm_mod'>, 'qpsk': <class 'gnuradio.digital.qpsk.qpsk_mod'>, 'dqpsk': <class 'gnuradio.digital.qpsk.dqpsk_mod'>, 'gfsk': <class 'gnuradio.digital.gfsk.gfsk_mod'>, 'qam': <class 'gnuradio.digital.qam.qam_mod'>, 'dbpsk': <class 'gnuradio.digital.bpsk.dbpsk_mod'>, 'bpsk': <class 'gnuradio.digital.bpsk.bpsk_mod'>, 'gmsk': <class 'gnuradio.digital.gmsk.gmsk_mod'>}
        #self.demods = {'psk': <class 'gnuradio.digital.psk.psk_demod'>, 'qpsk': <class 'gnuradio.digital.qpsk.qpsk_demod'>, 'dqpsk': <class 'gnuradio.digital.qpsk.dqpsk_demod'>, 'gfsk': <class 'gnuradio.digital.gfsk.gfsk_demod'>, 'qam': <class 'gnuradio.digital.qam.qam_demod'>, 'dbpsk': <class 'gnuradio.digital.bpsk.dbpsk_demod'>, 'bpsk': <class 'gnuradio.digital.bpsk.bpsk_demod'>, 'gmsk': <class 'gnuradio.digital.gmsk.gmsk_demod'>}
        #self.default_options()
        self.options = dotdict(opt)        
        self.options.samples_per_symbol = samples_per_symbol
        self.options.version = version
        self.options.antenna = antenna
        self.options.rx_freq = rx_freq
        self.options.rx_gain = rx_gain
        self.options.spec = spec
        self.options.tx_gain = tx_gain
        self.options.modulation = modulation
        self.options.args = args
        self.options.bitrate = bitrate
        self.options.tx_freq = tx_freq
        self.options.tx_amplitude = tx_amplitude
        
        self.rx_queue = Queue.Queue(12)
        self.tx_queue = Queue.Queue(12)
    
        print self.mods
        self.demodulator =self.demods[self.options.modulation]
        self.modulator = self.mods[self.options.modulation]
        self.tb_rx = TxRxLayer1.my_top_block_rx(self.demodulator, self.options,self.rx_queue)
        self.tb_tx = TxRxLayer1.my_top_block_tx(self.modulator, self.options,self.tx_queue)
        self.tb_rx.start()        # start flow graph
        self.tb_tx.start()
        return

    def run(self):
        self.readl2= self.ReadLayer2(self.ports_in[0], self.tx_queue)
        self.readl2.start()
        while not self.finished :
            frame = self.rx_queue.get()
            if not frame:
                print ' an empty frame from  L1 '
            else:
                event = if_events.mkevent("DataData")
                event.frmpkt = frame
                try:
                    for q in self.ports_out[0]:
                        q.put(event, False)   # add to queue, don't block  
                except Queue.Full:
                        print ' Layer 1 to Layer 2 queue is full, packet loss   ' 

        return


    def set_rx_freq(self,value):            
        self.tb_rx.set_freq(value)

    def set_tx_freq(self,value):            
        self.tb.set_freq(value)

    def sense_carrier(self):
        self.tb_rx.sense_carrier()


    def stop(self):
        self.readl2.stop()
        self.tb_tx.stop()
        self.tb_tx.wait()   
        print("tx top block stopped")
        self.tb_rx.stop()                    # wait for it to finis
        self.tb_rx.wait()         # wait for it to finish
        print("rx top block stopped")

    class ReadLayer2(threading.Thread):
        '''
        '''
        
        def __init__(self,in_queue,out_queue):
            '''  
            Constructor
            
            '''
            threading.Thread.__init__(self)
            self.in_queue = in_queue
            self.out_queue = out_queue
            self.finished = False            
            
        def run(self):
            ''' reads events, outputs frames.
            '''
            while not self.finished :
                event = self.in_queue.get()
                frame = event.frmpkt
                self.out_queue.put(frame)
            return
        def stop(self):
            self.finished = True
            self._Thread__stop()


class dotdict(dict):
        """dot.notation access to dictionary attributes"""
        def __getattr__(self, attr):
            return self.get(attr)
        __setattr__= dict.__setitem__
        __delattr__= dict.__delitem__        
        
def main():
    g = gwnGnuRadiopsk()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
