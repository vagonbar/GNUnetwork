#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Hier Tx
# Generated: Sun Oct  5 11:30:32 2014
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.filter import pfb
import math

class hier_tx(gr.hier_block2):

    def __init__(self, alfa=0.35, samp_per_sym=3, bits_per_sym=2, constellation=[-1-1j,1-1j, 1+1j, -1+1j], len_sym_srrc=7, out_const_mul=0.4):
        gr.hier_block2.__init__(
            self, "Hier Tx",
            gr.io_signature(1, 1, gr.sizeof_char*1),
            gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
        )

        ##################################################
        # Parameters
        ##################################################
        self.alfa = alfa
        self.samp_per_sym = samp_per_sym
        self.bits_per_sym = bits_per_sym
        self.constellation = constellation
        self.len_sym_srrc = len_sym_srrc
        self.out_const_mul = out_const_mul

        ##################################################
        # Variables
        ##################################################
        self.pulso = pulso = firdes.root_raised_cosine(samp_per_sym,samp_per_sym,1.0,alfa,samp_per_sym*len_sym_srrc)

        ##################################################
        # Blocks
        ##################################################
        self.pfb_interpolator_ccf_0 = pfb.interpolator_ccf(
        	  samp_per_sym,
        	  (pulso),
        	  100)
        	
        self.digital_diff_encoder_bb_0 = digital.diff_encoder_bb(2**bits_per_sym)
        self.digital_chunks_to_symbols_xx_0_0 = digital.chunks_to_symbols_bc((constellation), 1)
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(bits_per_sym, gr.GR_MSB_FIRST)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vcc((out_const_mul, ))

        ##################################################
        # Connections
        ##################################################
        self.connect((self.pfb_interpolator_ccf_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.digital_diff_encoder_bb_0, 0), (self.digital_chunks_to_symbols_xx_0_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_0, 0), (self.pfb_interpolator_ccf_0, 0))
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.digital_diff_encoder_bb_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self, 0))
        self.connect((self, 0), (self.blocks_packed_to_unpacked_xx_0, 0))


# QT sink close method reimplementation

    def get_alfa(self):
        return self.alfa

    def set_alfa(self, alfa):
        self.alfa = alfa
        self.set_pulso(firdes.root_raised_cosine(self.samp_per_sym,self.samp_per_sym,1.0,self.alfa,self.samp_per_sym*self.len_sym_srrc))

    def get_samp_per_sym(self):
        return self.samp_per_sym

    def set_samp_per_sym(self, samp_per_sym):
        self.samp_per_sym = samp_per_sym
        self.set_pulso(firdes.root_raised_cosine(self.samp_per_sym,self.samp_per_sym,1.0,self.alfa,self.samp_per_sym*self.len_sym_srrc))

    def get_bits_per_sym(self):
        return self.bits_per_sym

    def set_bits_per_sym(self, bits_per_sym):
        self.bits_per_sym = bits_per_sym

    def get_constellation(self):
        return self.constellation

    def set_constellation(self, constellation):
        self.constellation = constellation

    def get_len_sym_srrc(self):
        return self.len_sym_srrc

    def set_len_sym_srrc(self, len_sym_srrc):
        self.len_sym_srrc = len_sym_srrc
        self.set_pulso(firdes.root_raised_cosine(self.samp_per_sym,self.samp_per_sym,1.0,self.alfa,self.samp_per_sym*self.len_sym_srrc))

    def get_out_const_mul(self):
        return self.out_const_mul

    def set_out_const_mul(self, out_const_mul):
        self.out_const_mul = out_const_mul
        self.blocks_multiply_const_vxx_1.set_k((self.out_const_mul, ))

    def get_pulso(self):
        return self.pulso

    def set_pulso(self, pulso):
        self.pulso = pulso
        self.pfb_interpolator_ccf_0.set_taps((self.pulso))


