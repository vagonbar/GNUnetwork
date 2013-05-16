#!/usr/bin/env python
# -*- coding: utf-8 -*-

# formats-mac_mgmt : formats of MAC management frames.

'''Classes and functions for MAC Management frames.
'''

import frames
from frames import Frame
from mac_frcl import FCframe
from mac_data import DATAframe


class MgmtFrame(DATAframe): #Frame):
    '''Defines a Management frame.
    '''
    def __init__(self, mgmt_type=None, dc_fldvals={}):
        '''Builds a MgmtFrame object, updating field values for frame body field.

        @param mgmt_type: the Management frame type (Beacon, Action, etc.)        
        @param dc_fldvals: a dictionary of {field: value} to update field values.
        '''
        self.bitbyte='bytes'
        self.frame_len = 0
        self.mask_len = 0    # bytes, no bitmask
        self.ls_fields= ['frame_ctrl', 'duration', 'address_1', 'address_2', \
            #'address_3', 'seq_ctrl', 'ht', 'frame_body', 'fcs']
            'address_3', 'seq_ctrl', 'frame_body', 'fcs']
        dc_fields =  {\
            'frame_ctrl' : ( 0,  2,   False,   '!H' ), \
            'duration'   : ( 2,  4,   False,   '!H'  ), \
            'address_1'  : ( 4, 10,   False,   '!6s' ), \
            'address_2'  : (10, 16,   False,   '!6s' ), \
            'address_3'  : (16, 22,   False,   '!6s' ), \
            'seq_ctrl'   : (22, 24,   False,   '!H'  ), \
#            'ht'         : (24, 28,   False,   '!I'  ), \
#            'frame_body' : (28, 2342,  False,  '!s'  ), \
#            'ht'         : (24, 28,   False,   '!I'  ), \
            'frame_body' : (24, 2342,  False,  '!s'  ), \

            'fcs'        : (-4, None, False,  '!I'  )   \
            }
        self.mkdcfields(dc_fields)
        self.adjdatalen(dc_fldvals)        # adjust dc_fields template for data length
        self.dc_fldvals =  {  \
            'frame_ctrl' : 0, \
            'duration'   : 0, \
            'address_1'  : 'dt-ad1-', \
            'address_2'  : 'dt-ad2-', \
            'address_3'  : 'dt-ad3-', \
            'seq_ctrl'   : 0, \
#            'ht'         : 0, \
            'frame_body' : 'generic frame body', \
            'fcs'        : 0 \
            }
        #self.fillfldvals()
        self.dc_fldvals.update( FCframe.dc_frmtype['Beacon'] )
        self.dc_fldvals.update(dc_fldvals)
        return



class BeaconFrameBody(Frame):
    '''Frame body for Beacon MAC frame.

    Defines frame body for a Beacon MAC frame.
    '''
    def __init__(self, dc_fldvals={}):
        '''Builds an BeaconFrameBody object, updating field values for beacon frame body.
        @param dc_fldvals: a dictionary of {field: value} to update field values.
        '''
        self.bitbyte = 'bytes'
        self.frame_len = 58
        self.mask_len = 0    # bytes, no bitmask

        self.ls_fields = ['Timestamp', 'BeaconInterval', 'CapabilitiesInfo', 'SSID', 'SupportedRates']
        dc_fields              = {\
            'Timestamp'        : ( 0,  8, False, '!Q'  ), \
            'BeaconInterval'   : ( 8, 10, False, '!H'  ), \
            'CapabilitiesInfo' : (10, 12, False, '!H' ), \
            'SSID'             : (12, 46, False, '!34s' ), \
            'SupportedRates'   : (46, 58, False, '!12s'  ) \
            }
        self.mkdcfields(dc_fields)
        self.dc_fldvals        = { \
            'Timestamp'        :   1, \
            'BeaconInterval'   :  20, \
            'CapabilitiesInfo' :   0, \
            'SSID'             :  chr(0) + chr(32) + 'S'*32, 
                #struct.pack('!2c', 0 , 32) + 'S'*32, \
            'SupportedRates'   :  chr(1) + chr(10) + 'R'*10,
                #struct.pack('!2c', 0 , 10) +'R'*10 \
            }
        #self.fillfldvals()
        self.dc_fldvals.update( FCframe.dc_frmtype['Beacon'] )
        self.dc_fldvals.update(dc_fldvals)
         
        return


class ActionFrameBody(Frame):
    '''Frame body for Action MAC frame.

    Defines frame body for a Action MAC frame.
    IEEE 802.11-2012 sec 8.3.3.13 pag 436.
    '''

    def __init__(self, dc_fldvals={}):
        '''Builds an ActionFrameBody object, updating field values for action frame body.
        @param dc_fldvals: a dictionary of {field: value} to update field values.
        '''
        self.bitbyte = 'bytes'
        self.frame_len = 2  # variable if vendor specific parameters are present
        self.mask_len = 0    # bytes, no bitmask

        self.ls_fields = ['Action', 'MME']
        dc_fields = {\
            'Action' : ( 0,  1, False, '!B'  ), \
            'MME'    : (1,   2, False, '!B'  )  \
            }
        self.mkdcfields(dc_fields)
        self.dc_fldvals = { \
            'Action' :  0, \
            'MME'    :  0  \
            }
        #self.fillfldvals()
        self.dc_fldvals.update( FCframe.dc_frmtype['Action'] )
        self.dc_fldvals.update(dc_fldvals)
         
        return

