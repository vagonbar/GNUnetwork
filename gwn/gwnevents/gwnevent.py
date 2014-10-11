#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    This file is part of GNUWiNetwork,
#    Copyright (C) 2014 by 
#        Pablo Belzarena, Gabriel Gomez Sena, Victor Gonzalez Barbone,
#        Facultad de Ingenieria, Universidad de la Republica, Uruguay.
#
#    GNUWiNetwork is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    GNUWiNetwork is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with GNUWiNetwork.  If not, see <http://www.gnu.org/licenses/>.
#


'''A generic class for events of all types.

Class Event is a generic class for all types of events. Class Event is expected to be specialized into different, more specific types of events, implemented as subclasses. A hierarchy of event types and subtypes is possible. Events are distinguished by a nickname, a descriptive name used to recognize the type of event whatever their position in the event class hierarchy. Event nicknames are a convention of this project.

Nickname: 1. A descriptive name added to or replacing the actual name of a person, place, or thing (American Heritage Dictionary).

To create an event object use function C{events.mkevent()}. This function creates events of different types, according to the event modules imported by this module.
'''

import sys
import types

#import evtimer



sys.path = sys.path + ['..']



class Event:
    '''Events interchanged by blocks.

    Events are the objects interchanged by blocks in GWN. Events of a certain type are described by a nickname, from which type, subtype are determined. Nicknames are recorded in dictionary gwnevent_dc.dc_nicknames.
    @ivar nickname: a descriptive name to indicate the type of event.
    @ivar ev_type: the event type.
    @ivar ev_subtype: the event subtype.
    @ivar ev_dc: a dictionary of complementary data, e.g. {'add_info': 'additional information'}.
    '''

    def __init__(self, nickname, ev_type, ev_subtype, ev_dc={}):
        '''Constructor.
        
        @param nickname: a descriptive name to indicate the type of event.
        '''
        self.nickname = nickname
        self.ev_type = ev_type
        self.ev_subtype = ev_subtype
        self.ev_dc = ev_dc
        
    def __str__(self):
        ss = 'Event class name: ' + self.__class__.__name__
        ss += "\n  Nickname: '%s'; Type: '%s'; SubType: '%s'"  % \
            (self.nickname, self.ev_type, self.ev_subtype)
        for key in self.ev_dc.keys():
            #if key in ['src_addr', 'dst_addr']:
            #    ss += '\n  ' + key + ': ' + repr(self.ev_dc[key])
            #else:
            #    ss += '\n  ' + key + ': ' + str(self.ev_dc[key])
            ss += '\n  ' + key + ': ' + str(self.ev_dc[key])
        return ss


    def getname(self):
        '''Returns event nickname.
        
        TODO: see if really needed, nickname is public
        '''
        return self.nickname


class EventNameException(Exception):
    '''An exception to rise on non valid parameters for event construction.
    '''
    pass 





if __name__ == '__main__':
    import doctest
    doctest.testmod()


