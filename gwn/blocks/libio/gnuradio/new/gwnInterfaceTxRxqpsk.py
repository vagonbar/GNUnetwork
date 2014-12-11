#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    This file is part of GNUWiNetwork,
#    Copyright (C) 2014 by 
#        Pablo Belzarena, Gabriel Gomez Sena, Victor Gonzalez Barbone,
#        Facultad de Ingenieria, Universidad de la Republica, Uruguay.
#
#    GNUWiNetwork is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    GNUWiNetwork is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with GNUWiNetwork.  If not, see <http://www.gnu.org/licenses/>.
#

'''PSK modulation transmit / receive block.
'''

import sys
sys.path +=['..']

from gnuradio import digital
import gwnevents.api_events as api_events
import gwnTxRxL1_USRP as TxRxLayer1
import gwnblocks.gwnblock as gwn
import math



class QPSK(gwn.GWNBlock):
    '''PSK modulation block.
    '''

    def __init__(self, samples_per_symbol=5, antenna='TX/RX', \
        rx_freq=850000000.0, rx_gain=15.0, spec='A:0', tx_gain=15.0, \
        args='serial=E0R11Y0B1', bitrate=100000.0, \
        tx_freq=851000000.0, tx_amplitude=0.25):
        '''Constructor.
        
        '''
        super(QPSK,self).__init__(1, 'GNURadioChannelQPSK', 2, 2,1)
        #super(TunTapInterface, self).__init__(1,'TunTapInterface', 2, 2)
        self.set_timer(0, False, 3, 10)
        self.rx_conn = gwn.gwninport.AQueueConnector()
        self.tx_conn = gwn.gwninport.AQueueConnector()
        self.rx_queue = self.rx_conn.lsevents
        self.tx_queue = self.tx_conn.lsevents
        self.set_connection_in(self.rx_conn, 1)
        self.set_connection_out(self.tx_conn, 1)

        self.tb = TxRxLayer1.gwn_txrx_top_block(self.rx_queue,self.tx_queue,samples_per_symbol, antenna, \
        rx_freq, rx_gain, spec, tx_gain, \
        args, bitrate, \
        tx_freq, tx_amplitude,)
        self.tb.start()        # start flow graph
        return


    def process_data(self, port_type, port_nr, ev):
        '''Process data function for PSK block.
        '''
#        print " ------------------------------------"
#        print ev
#        print port_type,port_nr
#        print "-------------------------------------"
        # PRUEBA: EL TIMER ESTA PUESTO SOLO PARA PROBAR EL SENSADO
        if port_type == "intimer":
            self.sense_carrier()
        if port_type == 'inport' and port_nr == 0:
            frame = ev.frmpkt
            self.write_out(1, frame)    # 1, to GNU radio

        elif port_type == 'inport' and port_nr == 1:
            frame = ev   # ev is a frame received
            if not frame:
                print 'PSK: an empty frame from  L1'
            else:
                event = api_events.mkevent("DataData")
                event.frmpkt = frame
                self.write_out(0, event)

        return


    def set_rx_freq(self, value):
        '''Set receive frequency.
        '''
        self.tb_rx.set_freq(value)

    def set_tx_freq(self, value):
        '''Set transmit frequency.
        '''
        self.tb.set_freq(value)

    def sense_carrier(self):
        '''Sense carrier function.
        '''
        print " channel dbs sensed : "
        aux = self.tb.hier_rx_0.analog_probe_avg_mag_sqrd_x_0.level()
        if aux >0:
            print 10*math.log10(aux)

    def stop(self):
        '''PSK block stop function.

        This stop function is required to stop GNU Radio threads. Overwrites generic block stop function; first stops locally started threads, waits on them, and finally invokes the generic stop function in PSK super class (generic block).
        '''
        self.tb_tx.stop()
        self.tb_tx.wait()   
        print("tx top block stopped")
        self.tb_rx.stop()         # wait for it to finish
        self.tb_rx.wait()         # wait for it to finish
        print("rx top block stopped")
        super(ChannelQPSK, self).stop()


class dotdict(dict):
        '''dot.notation access to dictionary attributes.
        '''
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

