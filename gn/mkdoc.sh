#!/bin/bash
# mkdoc.sh: makes epydoc

EXCLUDES="viejos|otros|old|others|draft|libgwnBlocks|logs"
#EXCLUDES=$EXCLUDES"|libgnuradio|libadaptationlayer|libadaptlay80211|libevents|libframes|libfsm|libgnuradio|libMAC|libmac80211|libmacTDMA|libmanagement|libtimer|libutils|libvirtualchannel"
EXCLUDES=${EXCLUDES}"|libgnuradio|grc|scripts|xml"
EXCLUDES=${EXCLUDES}"|libfsm|libmanagement|libtimer"

if [ ! "$1" ]
then
  PRJNM=GNUWiNnetwork
  ##echo "Usage: mkdoc.sh <project name>"
else
  PRJNM="$1"
fi
if [ -d "html" ]
then
  rm -r html/*
else 
  mkdir html
fi
echo "  excluded:" $EXCLUDES
epydoc -v --name $PRJNM --exclude $EXCLUDES -o html lib* *.py

