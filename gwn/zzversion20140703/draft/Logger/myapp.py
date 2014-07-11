#!/usr/bin/env python
# -*- coding: utf-8 -*-

# myapp.py
import logging
import mylib

def main():
    #logging.basicConfig(filename='myapp.log', level=logging.INFO)
    fmtstr = '%(asctime)s %(name)s: %(message)s' 
    lvl = logging.DEBUG
    logging.basicConfig(filename='myapp.log', level=lvl, format=fmtstr)  

    logger = logging.getLogger('myapp')
    logger.info('Started')
    mylib.do_something()
    logger.info('Finished')

if __name__ == '__main__':
    main()



