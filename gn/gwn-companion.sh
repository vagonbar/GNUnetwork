#!/bin/bash
# gnuradio-companion.sh: invokes script of same name in subdir

THISDIR=`pwd`
cd ./grc/scripts
python ./gnuradio-companion.py
cd $THISDIR
