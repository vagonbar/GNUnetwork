#!/usr/bin/env python
# -*- coding: utf-8 -*-

# mac_ctrl.py


'''Classes and functions for MAC Control frames.

@var fc_obj: an FCframe object to invoke functions on without spending time in creating one object each time it is needed. Typical application is to obtain value of Frame Control field to insert in frames.
'''

import frames
from frames import Frame
from mac_frcl import FCframe

# a Frame Control object to invoke functions on
fc_obj = FCframe()


class RTSframe(Frame):
    '''RTS MAC frame.

    @param dc_fldvals: a dictionary of {field: value} to update field values.
    '''
    def __init__(self, dc_fldvals={}):
        '''Builds an RTSframe object, updating field values for RTS MAC frame.
        '''
        self.bitbyte = 'bytes'
        self.frame_len = 20
        self.mask_len = 0    # bytes, no bitmask

        self.ls_fields = ['frame_ctrl', 'duration', 'ra', 'ta', 'fcs']
        dc_fields        = {\
            'frame_ctrl' : ( 0,  2, False, '!H'  ), \
            'duration'   : ( 2,  4, False, '!H'  ), \
            'ra'         : ( 4, 10, False, '!6s' ), \
            'ta'         : (10, 16, False, '!6s' ), \
            'fcs'        : (16, 20, False, '!I'  ) \
            }
        self.mkdcfields(dc_fields)
        self.dc_fldvals = { \
            'frame_ctrl' : 0, \
            'duration'   : 0, \
            'ra'         : 'ra-rts', \
            'ta'         : 'ta-rts', \
            'fcs'         : 0 }
        # produce frame control field value from FCframe object
        fc_obj.setfctype('RTS')
        self.updtfldvals({'frame_ctrl':fc_obj.getfcint()})
        # update other field values
        self.dc_fldvals.update(dc_fldvals)
         
        return


class CTSframe(Frame):
    '''CTS MAC frame.

    @param dc_fldvals: a dictionary of {field: value} to update field values.
    '''
    def __init__(self, dc_fldvals={}):
        '''Builds a CTSframe object, updating field values for CTS MAC frame.
        '''
        self.bitbyte = 'bytes'
        self.frame_len = 14
        self.mask_len = 0    # bytes, no bitmask

        self.ls_fields = ['frame_ctrl', 'duration', 'ra', 'fcs']
        dc_fields        = {\
            'frame_ctrl' : ( 0,  2, False, '!H' ), \
            'duration'   : ( 2,  4, False, '!H'  ), \
            'ra'         : ( 4, 10, False, '!6s' ), \
            'fcs'        : (10, 14, False, '!I'  ) \
            }
        self.mkdcfields(dc_fields)
        self.dc_fldvals = { \
            'frame_ctrl' : 0, \
            'duration'   : 0, \
            'ra'         : 'ra-cts', \
            'fcs'         : 0 }

        # produce frame control field value from FCframe object
        fc_obj.setfctype('CTS')
        self.updtfldvals({'frame_ctrl':fc_obj.getfcint()})
        # update other field values
        self.dc_fldvals.update(dc_fldvals)
         
        return


class ACKframe(Frame):
    '''ACK MAC frame.
    '''
    def __init__(self, dc_fldvals={}):
        '''Builds an ACKframe object, updating field values for ACK MAC frame.
        
        @param dc_fldvals: a dictionary of {field: value} to update field values.
        '''    
        self.bitbyte = 'bytes'
        self.frame_len = 14
        self.mask_len = 0    # bytes, no bitmask

        self.ls_fields = ['frame_ctrl', 'duration', 'ra', 'fcs']
        dc_fields        = {\
            'frame_ctrl' : ( 0,  2, False, '!H' ), \
            'duration'   : ( 2,  4, False, '!H'  ), \
            'ra'         : ( 4, 10, False, '!6s' ), \
            'fcs'        : (10, 14, False, '!I'  ) \
            }
        self.mkdcfields(dc_fields)
        self.dc_fldvals = { \
            'frame_ctrl' : 0, \
            'duration'   : 0, \
            'ra'         : 'ra-ack', \
            'fcs'         : 0 }
        # produce frame control field value from FCframe object
        fc_obj.setfctype('ACK')
        self.updtfldvals({'frame_ctrl':fc_obj.getfcint()})
        # update other field values
        self.dc_fldvals.update(dc_fldvals)
         
        return



if __name__ == '__main__':
    import doctest
    print "mac_ctrl.py: running doctest file..."
    doctest.testfile('mac_ctrl.txt')
    print "mac_ctrl.py: ...done running doctest file. No messages means no errors on tests."



