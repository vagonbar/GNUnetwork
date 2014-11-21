#!/usr/bin/env python
#
# Copyright 2010,2011 Free Software Foundation, Inc.
# 
# This file is part of GNU Radio
# 
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

'''Transmit to and receive from layer 1.
'''
#execfile("/home/belza/.grc_gnuradio/hier_rx.py")
#execfile("/home/belza/.grc_gnuradio/hier_tx.py")
import hier_rx
import hier_tx
from gnuradio import channels
import gnuradio.gr.gr_threading as _threading
from gnuradio.digital import digital_swig as digital
from gnuradio import uhd
from gnuradio import blocks
from gnuradio import gr

import gwnpacket_utils as packet_utils

import  math
import threading,Queue


class gwn_txrx_top_block(gr.top_block):
    '''A top block for reception.
    '''
    def __init__(self,q_rx,q_tx,samp_per_sym=3, antenna='TX/RX', \
        rx_freq=850000000.0, rx_gain=15.0, spec='A:0', tx_gain=15.0, \
        args='serial=E0R11Y0B1', bit_rate=100000.0, \
        tx_freq=851000000.0, tx_amplitude=0.25,):
        '''Constructor.
        TODO: I AM NOT SETTING the Tx_AMPLITUDE
        @param q_rx:
        '''
        gr.top_block.__init__(self)
        self.sink_queue = gr.msg_queue()
        bits_per_sym = 2   # only for QPSK!
        #samp_per_sym=3
        sym_rate = bit_rate/bits_per_sym 
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	device_addr=args,
        	stream_args=uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_subdev_spec(spec, 0)
        self.uhd_usrp_source_0.set_center_freq(rx_freq, 0)
        self.uhd_usrp_source_0.set_gain(rx_gain, 0)
        self.uhd_usrp_source_0.set_antenna(antenna, 0)
        self.set_sample_rate(self.uhd_usrp_source_0,sym_rate, samp_per_sym)

        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	device_addr=args,
        	stream_args=uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_subdev_spec(spec, 0)
        self.uhd_usrp_sink_0.set_center_freq(tx_freq, 0)
        self.uhd_usrp_sink_0.set_gain(tx_gain, 0)
        self.uhd_usrp_sink_0.set_antenna(antenna, 0)
        self.set_sample_rate(self.uhd_usrp_sink_0,sym_rate, samp_per_sym)

        
        
        #self.Add(self.wxgui_scopesink2_0_0.win)
        self.hier_rx_0 = hier_rx.hier_rx(
            bw_clock_sync=2*math.pi/5,
            bw_fll=math.pi/400,
            bits_per_sym=bits_per_sym,
            bw_costas=2*math.pi/100,
            n_filts=32,
            len_sym_srrc=7,
            constellation=digital.constellation_calcdist([-1-1j, 1-1j, 1+1j, -1+1j], [], 4, 1).base(),
            samp_per_sym=samp_per_sym,
            alfa=0.35,
        )
        
        
        self.hier_tx_0 = hier_tx.hier_tx(
            alfa=0.35,
            samp_per_sym=samp_per_sym,
            constellation=[-1-1j,1-1j, 1+1j, -1+1j],
            len_sym_srrc=7,
            out_const_mul=0.4,
            bits_per_sym=bits_per_sym,
        )


        threshold = 12              # FIXME raise exception
        access_code = packet_utils.default_access_code
    
        self.blocks_message_source_0 = blocks.message_source(gr.sizeof_char*1, 4)
        self._rcvd_pktq = gr.msg_queue()          # holds packets from the PHY
        self.correlator = digital.correlate_access_code_bb( access_code, threshold)
        #"Arreglar access_code en la llamada a correlate""""""
        self.framer_sink = digital.framer_sink_1(self._rcvd_pktq)
        
        self.vsnk_src = blocks.vector_sink_b()
        self.m_sink   = blocks.message_sink(gr.sizeof_char*1, self.sink_queue,True)
        ##################################################
        # Connections
        ##################################################
        #self.connect((self.hier_tx_pencoder_0, 0), (self.wxgui_scopesink2_0_0, 0))
        self.connect(( self.blocks_message_source_0, 0),(self.hier_tx_0, 0) )
        self.connect((self.hier_tx_0, 0), (self.uhd_usrp_sink_0, 0))

        self.connect((self.uhd_usrp_source_0, 0), (self.hier_rx_0, 0))
        self.connect((self.hier_rx_0, 0), self.correlator, self.framer_sink)
        self._watcher = _queue_watcher_thread(self._rcvd_pktq,q_rx)
        queue = self.blocks_message_source_0.msgq()
        self.snd = SendData(q_tx,queue)   
    
#        self.connect((self.hier_rx_0, 0), (self.vsnk_src, 0))
#        self.connect((self.hier_rx_0, 0), (self.m_sink, 0))

    def set_sample_rate(self, usrp, sym_rate, req_sps):
        start_sps = req_sps
        while(True):
            asked_samp_rate = sym_rate * req_sps
            usrp.set_samp_rate(asked_samp_rate)
            actual_samp_rate = usrp.get_samp_rate()

            sps = actual_samp_rate/sym_rate
            if(sps < 2):
                req_sps +=1
            else:
                actual_sps = sps
                break
        
        if(True):
            print "\nSymbol Rate:         %f" % (sym_rate)
            print "Requested sps:       %f" % (start_sps)
            print "Given sample rate:   %f" % (actual_samp_rate)
            print "Actual sps for rate: %f" % (actual_sps)

        if(actual_samp_rate != asked_samp_rate):
            print "\nRequested sample rate: %f" % (asked_samp_rate)
            print "Actual sample rate: %f" % (actual_samp_rate)

        return (actual_samp_rate, actual_sps)

    def get_sample_rate(self,usrp):
        return usrp.get_samp_rate()




class SendData(threading.Thread) :
    '''The Beacon  is a Thread.
    
    This class controls the Beacon generation.       
    '''

    def __init__(self, q_tx,queue,samp_per_sym=3,bits_per_sym=2,preamble=None, access_code=None, msgq_limit=2,
                 pad_for_usrp=True, use_whitener_offset=False):
        '''  
        Constructor.
        '''

        threading.Thread.__init__(self)
        self._samp_per_sym =samp_per_sym
        self._bits_per_sym = bits_per_sym
        self._pad_for_usrp = pad_for_usrp
        self._use_whitener_offset = use_whitener_offset
        self._whitener_offset = 0
        
        if access_code is None:
            access_code = packet_utils.default_access_code
        if not packet_utils.is_1_0_string(access_code):
            raise ValueError, "Invalid access_code %r. Must be string of 1's and 0's" % (access_code,)
        self._access_code = access_code
        
        if preamble is None:
            preamble = packet_utils.default_preamble
        if not packet_utils.is_1_0_string(preamble):
            raise ValueError, "Invalid preamble %r. Must be string of 1's and 0's" % (preamble,)
        self._preamble = preamble
        self.finished = False        
        self.q_tx = q_tx
        self.my_queue =queue
        self.start()

    def send_pkt(self, payload='', eof=False):
        """
        Send the payload.

        Args:
            payload: data to send (string)
        """
        if eof:
            msg = gr.message(1) # tell self._pkt_input we're not sending any more packets
        else:
            # print "original_payload =", string_to_hex_list(payload)
            pkt = packet_utils.make_packet(payload,
                                           self._samp_per_sym,
                                           self._bits_per_sym,
                                           self._preamble,
                                           self._access_code,
                                           self._pad_for_usrp,
                                           self._whitener_offset)
            #print "pkt =", string_to_hex_list(pkt)
            msg = gr.message_from_string(pkt)
            if self._use_whitener_offset is True:
                self._whitener_offset = (self._whitener_offset + 1) % 16

        self.my_queue.insert_tail(msg)                
        #self._pkt_input.msgq().insert_tail(msg)

        
    def run(self):
        while not self.finished:
            payload= self.q_tx.get()
            self.send_pkt(payload)     

    def stop(self):
        self.finished = True
        self._Thread__stop()




class _queue_watcher_thread(_threading.Thread):
    def __init__(self, rcvd_pktq,q_rx):
        _threading.Thread.__init__(self)
        self.setDaemon(1)
        self.q_rx=q_rx
        self.rcvd_pktq = rcvd_pktq
        self.keep_running = True
        self.start()


    def run(self):
        while self.keep_running:
            msg = self.rcvd_pktq.delete_head()
            ok, payload = packet_utils.unmake_packet(msg.to_string(), int(msg.arg1()))
            print ok
            print payload
            if ok == True:
                self.q_rx.put(payload)


if __name__ == '__main__':
    
    q_rx = Queue.Queue()

    tb = gwn_sim_top_block(q_rx)
    tb.start()
    
#    n=0
#    pkt =0
#    print "inicio"
#    while n<4:
#        n=n+1
#        pkt = tb.sink_queue.delete_head().to_string()
#        print pkt
#        print '\n'
#    
#    print "fin"
#        
#    time.sleep(10)
#    data_src = scipy.array(tb.vsnk_src.data()[0:])    
#    print data_src
    tb.wait()
