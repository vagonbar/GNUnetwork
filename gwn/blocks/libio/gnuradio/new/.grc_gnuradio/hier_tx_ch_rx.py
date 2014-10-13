#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Hier Tx Ch Rx
# Generated: Sat Oct  4 09:50:38 2014
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import channels
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.filter import pfb
from grc_gnuradio import blks2 as grc_blks2
import math

class hier_tx_ch_rx(gr.hier_block2):

    def __init__(self):
        gr.hier_block2.__init__(
            self, "Hier Tx Ch Rx",
            gr.io_signature(1, 1, gr.sizeof_char*1),
            gr.io_signature(1, 1, gr.sizeof_char*1),
        )

        ##################################################
        # Variables
        ##################################################
        self.samp_per_sym = samp_per_sym = 3
        self.n_filts = n_filts = 32
        self.len_sym_srrc = len_sym_srrc = 7
        self.alfa = alfa = 0.35
        self.pulso = pulso = firdes.root_raised_cosine(samp_per_sym,samp_per_sym,1.0,alfa,samp_per_sym*len_sym_srrc)
        self.gain = gain = 15
        self.frec = frec = 850e3
        self.filtro_srrc = filtro_srrc = firdes.root_raised_cosine(n_filts,samp_per_sym*n_filts,1.0,alfa,samp_per_sym*len_sym_srrc*n_filts)
        self.bits_per_sym = bits_per_sym = 2

        ##################################################
        # Blocks
        ##################################################
        self.pfb_interpolator_ccf_0 = pfb.interpolator_ccf(
        	  samp_per_sym,
        	  (pulso),
        	  100)
        	
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(samp_per_sym, 2*math.pi/100, (filtro_srrc), n_filts, 16, 5, 1)
        self.digital_fll_band_edge_cc_0 = digital.fll_band_edge_cc(samp_per_sym, alfa, len_sym_srrc*samp_per_sym, math.pi/1600)
        self.digital_diff_encoder_bb_0 = digital.diff_encoder_bb(2**bits_per_sym)
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(2**bits_per_sym)
        self.digital_costas_loop_cc_0_0_0 = digital.costas_loop_cc(2*math.pi/100, 2**bits_per_sym)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb( digital.constellation_calcdist([-1-1j, 1-1j, 1+1j, -1+1j], [], 4, 1).base())
        self.digital_chunks_to_symbols_xx_0_0 = digital.chunks_to_symbols_bc(([-1-1j,1-1j, 1+1j, -1+1j]), 1)
        self.channels_channel_model_0 = channels.channel_model(
        	noise_voltage=0.0,
        	frequency_offset=0.0,
        	epsilon=1.00,
        	taps=(1+0.5j, ),
        	noise_seed=0,
        	block_tags=False
        )
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(bits_per_sym)
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(bits_per_sym, gr.GR_MSB_FIRST)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vcc((0.4, ))
        self.blks2_packet_encoder_0 = grc_blks2.packet_mod_b(grc_blks2.packet_encoder(
        		samples_per_symbol=samp_per_sym,
        		bits_per_symbol=bits_per_sym,
        		preamble="",
        		access_code="",
        		pad_for_usrp=True,
        	),
        	payload_length=1,
        )
        self.blks2_packet_decoder_0 = grc_blks2.packet_demod_b(grc_blks2.packet_decoder(
        		access_code="",
        		threshold=-1,
        		callback=lambda ok, payload: self.blks2_packet_decoder_0.recv_pkt(ok, payload),
        	),
        )
        self.analog_agc2_xx_0 = analog.agc2_cc(1e-1, 1e-2, 1.0, 1.0)
        self.analog_agc2_xx_0.set_max_gain(65536)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.pfb_interpolator_ccf_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.digital_diff_encoder_bb_0, 0), (self.digital_chunks_to_symbols_xx_0_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_0, 0), (self.pfb_interpolator_ccf_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.channels_channel_model_0, 0))
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.digital_diff_encoder_bb_0, 0))
        self.connect((self.blks2_packet_encoder_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.blks2_packet_decoder_0, 0))
        self.connect((self.blks2_packet_decoder_0, 0), (self, 0))
        self.connect((self, 0), (self.blks2_packet_encoder_0, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.digital_costas_loop_cc_0_0_0, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.analog_agc2_xx_0, 0), (self.digital_fll_band_edge_cc_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.analog_agc2_xx_0, 0))
        self.connect((self.digital_fll_band_edge_cc_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_costas_loop_cc_0_0_0, 0))


# QT sink close method reimplementation

    def get_samp_per_sym(self):
        return self.samp_per_sym

    def set_samp_per_sym(self, samp_per_sym):
        self.samp_per_sym = samp_per_sym
        self.set_pulso(firdes.root_raised_cosine(self.samp_per_sym,self.samp_per_sym,1.0,self.alfa,self.samp_per_sym*self.len_sym_srrc))
        self.set_filtro_srrc(firdes.root_raised_cosine(self.n_filts,self.samp_per_sym*self.n_filts,1.0,self.alfa,self.samp_per_sym*self.len_sym_srrc*self.n_filts))

    def get_n_filts(self):
        return self.n_filts

    def set_n_filts(self, n_filts):
        self.n_filts = n_filts
        self.set_filtro_srrc(firdes.root_raised_cosine(self.n_filts,self.samp_per_sym*self.n_filts,1.0,self.alfa,self.samp_per_sym*self.len_sym_srrc*self.n_filts))

    def get_len_sym_srrc(self):
        return self.len_sym_srrc

    def set_len_sym_srrc(self, len_sym_srrc):
        self.len_sym_srrc = len_sym_srrc
        self.set_pulso(firdes.root_raised_cosine(self.samp_per_sym,self.samp_per_sym,1.0,self.alfa,self.samp_per_sym*self.len_sym_srrc))
        self.set_filtro_srrc(firdes.root_raised_cosine(self.n_filts,self.samp_per_sym*self.n_filts,1.0,self.alfa,self.samp_per_sym*self.len_sym_srrc*self.n_filts))

    def get_alfa(self):
        return self.alfa

    def set_alfa(self, alfa):
        self.alfa = alfa
        self.set_pulso(firdes.root_raised_cosine(self.samp_per_sym,self.samp_per_sym,1.0,self.alfa,self.samp_per_sym*self.len_sym_srrc))
        self.set_filtro_srrc(firdes.root_raised_cosine(self.n_filts,self.samp_per_sym*self.n_filts,1.0,self.alfa,self.samp_per_sym*self.len_sym_srrc*self.n_filts))

    def get_pulso(self):
        return self.pulso

    def set_pulso(self, pulso):
        self.pulso = pulso
        self.pfb_interpolator_ccf_0.set_taps((self.pulso))

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain

    def get_frec(self):
        return self.frec

    def set_frec(self, frec):
        self.frec = frec

    def get_filtro_srrc(self):
        return self.filtro_srrc

    def set_filtro_srrc(self, filtro_srrc):
        self.filtro_srrc = filtro_srrc
        self.digital_pfb_clock_sync_xxx_0.set_taps((self.filtro_srrc))

    def get_bits_per_sym(self):
        return self.bits_per_sym

    def set_bits_per_sym(self, bits_per_sym):
        self.bits_per_sym = bits_per_sym


