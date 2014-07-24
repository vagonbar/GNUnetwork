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
#import Queue
#import threading
import gwnevents.if_events as if_events
import TxRxLayer1 as TxRxLayer1
import gwnblocks.gwnblock as gwn


class PSK(gwn.GWNBlock):

    def __init__(self, samples_per_symbol=2, version='6', antenna='TX/RX', \
        rx_freq=850000000.0, rx_gain=15.0, spec='A:0', tx_gain=15.0, \
        modulation='bpsk', args='serial=E0R11Y0B1', bitrate=100000.0, \
        tx_freq=851000000.0, tx_amplitude=0.25):
        '''Constructor.
        '''
        super(PSK,self).__init__(1, 'GNURadioPSK', 1, 1)
        #super(TunTapInterface, self).__init__(1,'TunTapInterface', 2, 2)
        self.mods = digital.modulation_utils.type_1_mods()
        self.demods = digital.modulation_utils.type_1_demods()
        opt = {'verbose':True, 'samples_per_symbol':2, 'chbw_factor':1.0, 'log':False, 'version':'6', 'antenna':'TX/RX', 'rx_freq':850000000.0, 'version':'6', 'rx_gain':15.0, 'spec':'A:0', 'tx_gain':15.0, 'modulation':'bpsk', 'args':'serial=E0R11Y0B1', 'freq':None, 'bitrate':100000.0, 'from_file':None, 'to_file':None, 'tx_freq':851000000.0, 'tx_amplitude':0.25}        
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

        self.rx_conn = gwn.gwninport.AQueueConnector()
        self.tx_conn = gwn.gwninport.AQueueConnector()
        self.rx_queue = self.rx_conn.lsevents
        self.tx_queue = self.tx_conn.lsevents
        self.set_connection_in(self.rx_conn, 1)
        self.set_connection_out(self.tx_conn, 1)

        print 'PSK:', self.mods
        self.demodulator = self.demods[self.options.modulation]
        self.modulator = self.mods[self.options.modulation]
        self.tb_rx = TxRxLayer1.my_top_block_rx(self.demodulator, \
            self.options, self.rx_queue)
        self.tb_tx = TxRxLayer1.my_top_block_tx(self.modulator, \
            self.options, self.tx_queue)
        self.tb_rx.start()        # start flow graph
        self.tb_tx.start()
        return


    def process_data(self, port_type, port_nr, ev):
        #self.readl2= self.ReadLayer2(self.ports_in[0], self.tx_queue)
        #self.readl2.start()
        #while not self.finished :
        if port_type == 'InPort' and port_nr == 0:
            frame = ev.frmpkt
            self.write_out(1, frame)    # 1, to GNU radio

        elif port_type == 'InPort' and port_nr == 1:
            frame = ev   # ev is a frame received
            if not frame:
                print 'PSK: an empty frame from  L1'
            else:
                event = if_events.mkevent("DataData")
                event.frmpkt = frame
                self.write_out(0, event)
        return


    def set_rx_freq(self, value):
        self.tb_rx.set_freq(value)

    def set_tx_freq(self, value):
        self.tb.set_freq(value)

    def sense_carrier(self):
        self.tb_rx.sense_carrier()

    def stop(self):
        self.tb_tx.stop()
        self.tb_tx.wait()   
        print("tx top block stopped")
        self.tb_rx.stop()         # wait for it to finish
        self.tb_rx.wait()         # wait for it to finish
        print("rx top block stopped")
        super(PSK, self).stop()


class dotdict(dict):
        """dot.notation access to dictionary attributes"""
        def __getattr__(self, attr):
            return self.get(attr)
        __setattr__= dict.__setitem__
        __delattr__= dict.__delitem__        

        
def main():
    g = PSK()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
