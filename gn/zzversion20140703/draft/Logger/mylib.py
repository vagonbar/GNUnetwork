#!/usr/bin/env python
# -*- coding: utf-8 -*-

# mylib.py

import myapp

import logging
logger = logging.getLogger(__name__)

def do_something():
    logger.info('Doing something, in logger')
    #logging.info('Doing something, in logging')


if __name__ == '__main__':
    myapp.main()
    do_something()
