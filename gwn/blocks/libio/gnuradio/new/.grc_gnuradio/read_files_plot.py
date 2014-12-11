# -*- coding: utf-8 -*-
"""
Created on Sun Nov 23 08:54:25 2014

@author: belza
"""

import scipy
from gnuradio import gr
from gnuradio import blocks
import matplotlib.pyplot as plt



def frombitstohex(bits):
    vbytes = []
    for b in range(len(bits) / 8):
        byte = bits[b*8:(b+1)*8]
        i=0
        res=0
        for bit in byte:
            #print bit
            res=res+bit*2**(7-i)
            #print res
            i=i+1
        #print "resultado"
        #print res    
        hres= hex(res)
        vbytes.append(hres)
    return vbytes

def frombits(bits):
    vbytes = []
    for b in range(len(bits) / 8):
        byte = bits[b*8:(b+1)*8]
        i=0
        res=0
        for bit in byte:
            #print bit
            res=res+bit*2**(7-i)
            #print res
            i=i+1
        #print "resultado"
        #print res    
        vbytes.append(res)
    return vbytes

    
def main():
    """
    gr.sizeof_char: 1 byte per sample, f = scipy.fromfile(open("filename"), dtype=scipy.uint8)
    gr.sizeof_short: 2 bytes per sample, f = scipy.fromfile(open("filename"), dtype=scipy.int16)
    gr.sizeof_int: 4 bytes per sample, f = scipy.fromfile(open("filename"), dtype=scipy.int32)
    gr.sizeof_float: 4 bytes per sample (IEEE 754 single-precision floats), f = scipy.fromfile(open("filename"), dtype=scipy.float32)
    gr.sizeof_gr_complex: 4 bytes per sample as floating point real and imaginary, f = scipy.fromfile(open("filename"), dtype=scipy.complex64)
    """

#    f = scipy.fromfile(open("/home/belza/pruebasUSRP/file_rx_fin"), dtype=scipy.uint8)
#    print f[0:100]
#    plt.plot(f[0:100], 'ro')
#    #plt.axis([0, 6, 0, 20])
#    plt.show()
#    aux = frombits(f[4:])
#    print aux
#    print len(aux)
#    plt.figure(1)
#    plt.plot(aux[1:500], 'ro')
#    state =0    
#    count =0
#    count2=0
#    for x in aux:
#        count2 = count2+1
#        if x == 85:
#            state = state +1
#            if state == 20:
#                count = count +1
#                state = 0
#                print aux[count2-250:count2]
#                print count
#                print count2
#                print "----------------------------------------------------------------------------"
#        else:
#            state =0
#
#
#    f = scipy.fromfile(open("/home/belza/pruebasUSRP/file_tx_ini"), dtype=scipy.uint8)
#    print f[1:1000]
#    plt.plot(f[0:100], 'ro') 
#    #plt.axis([0, 6, 0, 20])
#    plt.show()



#    f = scipy.fromfile(open("/home/belza/Dropbox/gn/gwn/blocks/libio/gnuradio/new/.grc_gnuradio/file_tx_2bits"), dtype=scipy.uint8)
#    print f[1:100]

    plt.figure(2) 
    f1 = scipy.fromfile(open("/home/belza/pruebasUSRP/file_tx_out"), dtype=scipy.complex64)
#    print f1[1:100]
    plt.plot(real(f1[1:10000]), 'ro')
##   plt.axis([0, 6, 0, 20])
    plt.plot(imag(f1[1:10000]),'+')
#
    plt.figure(3)
    f2 = scipy.fromfile(open("/home/belza/pruebasUSRP/file_rx_sym"), dtype=scipy.complex64)
    #print f2[1:10000]
    plt.plot(real(f2), 'ro')
   
    plt.plot(imag(f2),'+')
#
#    plt.figure(3)
#    f3 = scipy.fromfile(open("/home/belza/pruebasUSRP/file_rx_sym"), dtype=scipy.complex64)
##    print f3[1:100]
#    plt.plot(real(f3), 'ro')
##   plt.axis([0, 6, 0, 20])
#    plt.plot(imag(f3),'+')

    
    plt.show()
    
    

if __name__ == "__main__":
    main()