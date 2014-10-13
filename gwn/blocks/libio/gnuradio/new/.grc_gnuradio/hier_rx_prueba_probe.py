#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Hier Rx
# Generated: Sun Oct  5 11:30:37 2014
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
from gnuradio import filter
import math

class hier_rx(gr.hier_block2):

    def __init__(self, bw_clock_sync=2*math.pi/100, bw_fll=math.pi/1600, bits_per_sym=2, bw_costas=2*math.pi/100, n_filts=32, len_sym_srrc=7, constellation=digital.constellation_calcdist([-1-1j, 1-1j, 1+1j, -1+1j], [], 4, 1).base(), samp_per_sym=3, alfa=0.35):
        gr.hier_block2.__init__(
            self, "Hier Rx",
            gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
            gr.io_signature(1, 1, gr.sizeof_char*1),
        )

        ##################################################
        # Parameters
        ##################################################
        self.bw_clock_sync = bw_clock_sync
        self.bw_fll = bw_fll
        self.bits_per_sym = bits_per_sym
        self.bw_costas = bw_costas
        self.n_filts = n_filts
        self.len_sym_srrc = len_sym_srrc
        self.constellation = constellation
        self.samp_per_sym = samp_per_sym
        self.alfa = alfa

        ##################################################
        # Variables
        ##################################################
        self.filtro_srrc = filtro_srrc = firdes.root_raised_cosine(n_filts,samp_per_sym*n_filts,1.0,alfa,samp_per_sym*len_sym_srrc*n_filts)

        ##################################################
        # Blocks
        ##################################################
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(samp_per_sym, bw_clock_sync, (filtro_srrc), n_filts, 16, 5, 1)
        self.digital_fll_band_edge_cc_0 = digital.fll_band_edge_cc(samp_per_sym, alfa, len_sym_srrc*samp_per_sym, bw_fll)
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(2**bits_per_sym)
        self.digital_costas_loop_cc_0_0_0 = digital.costas_loop_cc(bw_costas, 2**bits_per_sym)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(constellation)
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(bits_per_sym)
        self.analog_agc2_xx_0 = analog.agc2_cc(1e-1, 1e-2, 1.0, 1.0)
        self.analog_agc2_xx_0.set_max_gain(65536)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.analog_agc2_xx_0, 0), (self.digital_fll_band_edge_cc_0, 0))
        self.connect((self.digital_fll_band_edge_cc_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_costas_loop_cc_0_0_0, 0))
        self.connect((self, 0), (self.analog_agc2_xx_0, 0))
        self.connect((self.digital_costas_loop_cc_0_0_0, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self, 0))

        sw_decim = 1
        self._chbw_factor=1
        chan_coeffs = filter.firdes.low_pass (1.0,                  # gain
                                          sw_decim * self.samp_per_sym, # sampling rate
                                          self._chbw_factor,    # midpoint of trans. band
                                          0.5,                  # width of trans. band
                                          filter.firdes.WIN_HANN)   # filter type
        self.channel_filter = filter.fft_filter_ccc(sw_decim, chan_coeffs)
        
        # Carrier Sensing Blocks
        alpha = 0.001
        thresh = 30   # in dB, will have to adjust
        self.probe = analog.probe_avg_mag_sqrd_c(thresh,alpha)

        self.connect(self, self.channel_filter)

        # connect the channel input filter to the carrier power detector
        self.connect(self.channel_filter, self.probe)

    def carrier_sensed(self):
        """
        Return True if we think carrier is present.
        """
        #return self.probe.level() > X
        return self.probe.level()

    def carrier_threshold(self):
        """
        Return current setting in dB.
        """
        return self.probe.threshold()

    def set_carrier_threshold(self, threshold_in_db):
        """
        Set carrier threshold.

        @param threshold_in_db: set detection threshold
        @type threshold_in_db:  float (dB)
        """
        self.probe.set_threshold(threshold_in_db)


# QT sink close method reimplementation

    def get_bw_clock_sync(self):
        return self.bw_clock_sync

    def set_bw_clock_sync(self, bw_clock_sync):
        self.bw_clock_sync = bw_clock_sync
        self.digital_pfb_clock_sync_xxx_0.set_loop_bandwidth(self.bw_clock_sync)

    def get_bw_fll(self):
        return self.bw_fll

    def set_bw_fll(self, bw_fll):
        self.bw_fll = bw_fll
        self.digital_fll_band_edge_cc_0.set_loop_bandwidth(self.bw_fll)

    def get_bits_per_sym(self):
        return self.bits_per_sym

    def set_bits_per_sym(self, bits_per_sym):
        self.bits_per_sym = bits_per_sym

    def get_bw_costas(self):
        return self.bw_costas

    def set_bw_costas(self, bw_costas):
        self.bw_costas = bw_costas
        self.digital_costas_loop_cc_0_0_0.set_loop_bandwidth(self.bw_costas)

    def get_n_filts(self):
        return self.n_filts

    def set_n_filts(self, n_filts):
        self.n_filts = n_filts
        self.set_filtro_srrc(firdes.root_raised_cosine(self.n_filts,self.samp_per_sym*self.n_filts,1.0,self.alfa,self.samp_per_sym*self.len_sym_srrc*self.n_filts))

    def get_len_sym_srrc(self):
        return self.len_sym_srrc

    def set_len_sym_srrc(self, len_sym_srrc):
        self.len_sym_srrc = len_sym_srrc
        self.set_filtro_srrc(firdes.root_raised_cosine(self.n_filts,self.samp_per_sym*self.n_filts,1.0,self.alfa,self.samp_per_sym*self.len_sym_srrc*self.n_filts))

    def get_constellation(self):
        return self.constellation

    def set_constellation(self, constellation):
        self.constellation = constellation

    def get_samp_per_sym(self):
        return self.samp_per_sym

    def set_samp_per_sym(self, samp_per_sym):
        self.samp_per_sym = samp_per_sym
        self.set_filtro_srrc(firdes.root_raised_cosine(self.n_filts,self.samp_per_sym*self.n_filts,1.0,self.alfa,self.samp_per_sym*self.len_sym_srrc*self.n_filts))

    def get_alfa(self):
        return self.alfa

    def set_alfa(self, alfa):
        self.alfa = alfa
        self.set_filtro_srrc(firdes.root_raised_cosine(self.n_filts,self.samp_per_sym*self.n_filts,1.0,self.alfa,self.samp_per_sym*self.len_sym_srrc*self.n_filts))

    def get_filtro_srrc(self):
        return self.filtro_srrc

    def set_filtro_srrc(self, filtro_srrc):
        self.filtro_srrc = filtro_srrc
        self.digital_pfb_clock_sync_xxx_0.set_taps((self.filtro_srrc))


