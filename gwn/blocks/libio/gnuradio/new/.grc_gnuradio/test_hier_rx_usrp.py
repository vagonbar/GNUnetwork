#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Test Hier Rx Usrp
# Generated: Mon Dec  8 10:33:31 2014
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import math
import time
import wx

class test_hier_rx_usrp(grc_wxgui.top_block_gui):

    def __init__(self, n_filts=32, bits_per_sym=2, alpha_probe=0.1, th_probe=0, constellation=digital.constellation_calcdist([-1-1j, 1-1j, 1+1j, -1+1j], [], 4, 1).base(), samp_per_sym=5, bw_costas=2*math.pi/100, bw_clock_sync=2*math.pi/100, bw_fll=2*math.pi/100, len_sym_srrc=11, alfa=0.45):
        grc_wxgui.top_block_gui.__init__(self, title="Test Hier Rx Usrp")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Parameters
        ##################################################
        self.n_filts = n_filts
        self.bits_per_sym = bits_per_sym
        self.alpha_probe = alpha_probe
        self.th_probe = th_probe
        self.constellation = constellation
        self.samp_per_sym = samp_per_sym
        self.bw_costas = bw_costas
        self.bw_clock_sync = bw_clock_sync
        self.bw_fll = bw_fll
        self.len_sym_srrc = len_sym_srrc
        self.alfa = alfa

        ##################################################
        # Variables
        ##################################################
        self.filtro_srrc = filtro_srrc = firdes.root_raised_cosine(n_filts,samp_per_sym*n_filts,1.0,alfa,samp_per_sym*len_sym_srrc*n_filts)

        ##################################################
        # Blocks
        ##################################################
        self.wxgui_scopesink2_0 = scopesink2.scope_sink_c(
        	self.GetWin(),
        	title="Scope Plot",
        	sample_rate=250000/samp_per_sym,
        	v_scale=0.3,
        	v_offset=0,
        	t_scale=0.3,
        	ac_couple=False,
        	xy_mode=True,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label="Counts",
        )
        self.Add(self.wxgui_scopesink2_0.win)
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	device_addr="",
        	stream_args=uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(50000*samp_per_sym)
        self.uhd_usrp_source_0.set_center_freq(850000000, 0)
        self.uhd_usrp_source_0.set_gain(18, 0)
        self.uhd_usrp_source_0.set_antenna("TX/RX", 0)
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(samp_per_sym, bw_clock_sync, (filtro_srrc), n_filts, 16, 5, 1)
        self.digital_mpsk_snr_est_cc_0 = digital.mpsk_snr_est_cc(0, 10000, 0.001)
        self.digital_fll_band_edge_cc_0 = digital.fll_band_edge_cc(samp_per_sym, alfa, len_sym_srrc*samp_per_sym, bw_fll)
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(2**bits_per_sym)
        self.digital_costas_loop_cc_0_0_0 = digital.costas_loop_cc(bw_costas, 2**bits_per_sym)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(constellation)
        self.blocks_vector_sink_x_0 = blocks.vector_sink_b(1)
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(bits_per_sym)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_gr_complex*1, "/home/belza/pruebasUSRP/file_rx_sym", False)
        self.blocks_file_sink_0_0.set_unbuffered(True)
        self.analog_agc2_xx_0 = analog.agc2_cc(0.6e-1, 1e-3, 2, 15)
        self.analog_agc2_xx_0.set_max_gain(15)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.analog_agc2_xx_0, 0), (self.digital_fll_band_edge_cc_0, 0))
        self.connect((self.digital_fll_band_edge_cc_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.analog_agc2_xx_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.blocks_vector_sink_x_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_costas_loop_cc_0_0_0, 0))
        self.connect((self.digital_costas_loop_cc_0_0_0, 0), (self.blocks_file_sink_0_0, 0))
        self.connect((self.digital_costas_loop_cc_0_0_0, 0), (self.wxgui_scopesink2_0, 0))
        self.connect((self.digital_costas_loop_cc_0_0_0, 0), (self.digital_mpsk_snr_est_cc_0, 0))
        self.connect((self.digital_mpsk_snr_est_cc_0, 0), (self.digital_constellation_decoder_cb_0, 0))


# QT sink close method reimplementation

    def get_n_filts(self):
        return self.n_filts

    def set_n_filts(self, n_filts):
        self.n_filts = n_filts
        self.set_filtro_srrc(firdes.root_raised_cosine(self.n_filts,self.samp_per_sym*self.n_filts,1.0,self.alfa,self.samp_per_sym*self.len_sym_srrc*self.n_filts))

    def get_bits_per_sym(self):
        return self.bits_per_sym

    def set_bits_per_sym(self, bits_per_sym):
        self.bits_per_sym = bits_per_sym

    def get_alpha_probe(self):
        return self.alpha_probe

    def set_alpha_probe(self, alpha_probe):
        self.alpha_probe = alpha_probe

    def get_th_probe(self):
        return self.th_probe

    def set_th_probe(self, th_probe):
        self.th_probe = th_probe

    def get_constellation(self):
        return self.constellation

    def set_constellation(self, constellation):
        self.constellation = constellation

    def get_samp_per_sym(self):
        return self.samp_per_sym

    def set_samp_per_sym(self, samp_per_sym):
        self.samp_per_sym = samp_per_sym
        self.set_filtro_srrc(firdes.root_raised_cosine(self.n_filts,self.samp_per_sym*self.n_filts,1.0,self.alfa,self.samp_per_sym*self.len_sym_srrc*self.n_filts))
        self.wxgui_scopesink2_0.set_sample_rate(250000/self.samp_per_sym)
        self.uhd_usrp_source_0.set_samp_rate(50000*self.samp_per_sym)

    def get_bw_costas(self):
        return self.bw_costas

    def set_bw_costas(self, bw_costas):
        self.bw_costas = bw_costas
        self.digital_costas_loop_cc_0_0_0.set_loop_bandwidth(self.bw_costas)

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

    def get_len_sym_srrc(self):
        return self.len_sym_srrc

    def set_len_sym_srrc(self, len_sym_srrc):
        self.len_sym_srrc = len_sym_srrc
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
class test_snr(threading.Thread):
    '''A control thread for transmission / reception into layer 1.
    '''
    
    def __init__(self, tb):
        '''Constructor.
        
        @param tb:
        '''
        threading.Thread.__init__(self)
        self.tb = tb
        self.finished = False

    def run(self):
        while not self.finished:
            snr= tb.digital_mpsk_snr_est_cc_0.snr()
            print " -------------------------------------------------"
            print "SNR : "
	    print snr
            print "--------------------------------------------------"
            time.delay(10)    
                
    def stop(self):
        self.finished=True
        self._Thread__stop()
  
if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = test_hier_rx_usrp()
    tb.Start(True)
    tb.Wait()

