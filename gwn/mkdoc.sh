#!/bin/bash
# mkdoc.sh: makes epydoc

#ALLSUBDIRS="bitacora_belza.txt|doc|draft|grc|gwn-companion.sh|html|__init__.py|__init__.pyc|libadaptationlayer|libadaptlay80211|libevents|libframes|libfsm|libgnuradio|libgwnblocks|libgwnBlocks|libMAC|libmac80211|libmacTDMA|libmanagement|libtimer|libutils|libvirtualchannel|logs|mkdoc.sh|runtests.py|runtests.pyc|runtests.sh|scripts|xml|"

EXCLUDES="viejos|otros|old|others|draft|libgwnBlocks|logs"

#EXCLUDES=${EXCLUDES}"|bitacora_belza.txt"
#EXCLUDES=${EXCLUDES}"|mac_action"
EXCLUDES=${EXCLUDES}"|libgnuradio|grc|scripts|xml"
#EXCLUDES=${EXCLUDES}"|libfsm|libmanagement|libtimer"

#EXCLUDES="bitacora_belza.txt|draft|grc|gwn-companion.sh|libadaptationlayer|libadaptlay80211|libevents|libframes|libfsm|libgnuradio|libgwnBlocks|libMAC|libmac80211|libmacTDMA|libmanagement|libtimer|libvirtualchannel|logs|runtests.py|scripts|xml"




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

### ERROR: with full content nothing was generated!
# opted for generating only updated versions of code
#echo "  excluded:" $EXCLUDES
#epydoc -v --name $PRJNM -o ./html --exclude "$EXCLUDES" gn


# the files to include in doc generation

#INCLUDES="__init__.py libgwnblocks doc libvirtualchannel"
#epydoc -v --name $PRJNM $INCLUDES
#/usr/share/pyshared/epydoc/cli -v --name $PRJNM

PYTHONPATH=$PYTHONPATH:/usr/share/pyshared/
env PYTHONPATH=$PYTHONPATH:/usr/share/pyshared/ python /usr/share/pyshared/epydoc/cli.py -v --name GNUWiNetwork --exclude "gwnc" .



