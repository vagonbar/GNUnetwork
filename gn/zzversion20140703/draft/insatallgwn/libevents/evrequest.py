#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Classes and functions to handle events for bloks configuration.

@var dc_nicknames: a dictionary of nicknames, types, subtypes, and classnames, C{ {nickname: (type, subtype, classname)} }; C{classname} is the class used to build the object. This dictionary allows to build a time event object by just saying its nickname. Module function C{mkevent()} uses this module variable.
'''

from events import Event, EventNameException



class EventRequest(Event):
    '''An event associated with the configuration of blocks.
    
    @ivar nickname: a descriptive name for this event.
    @ivar ev_type: timer event type.
    @ivar ev_subtype: timer event subtype.
    @ivar ev_dc: a dictionary of complementary data, e.g. {'add_info': 'additional information'}.
    '''
    
    def __init__(self, nickname, ev_type, ev_subtype, ev_dc={}):
        '''Constructor.
        '''
        self.nickname = nickname
        self.ev_type = ev_type
        self.ev_subtype = ev_subtype
        self.ev_dc = {}
        self.ev_dc.update(ev_dc)
        return




dc_nicknames = { \
	'TimerConfig'        : ('Request',  'SetTimerConfig',     EventRequest     ), \
	'EventConsumerStatus'  : ('Request',  'EventConsumerStatus', EventRequest     ) \
    }



if __name__ == '__main__':
    import doctest
    doctest.testmod()

