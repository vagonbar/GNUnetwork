#!/bin/bash
# mkdoc.sh: makes epydoc


EXCLUDES="viejos|otros|old|others|draft|logs"

EXCLUDES=${EXCLUDES}"|gwnc|scripts|xml"

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

epydoc -v --name $PRJNM -o ./html --exclude "$EXCLUDES" .
