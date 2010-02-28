#!/usr/bin/env python

# Copyright (c) 2010, Fresno Pacific University
# Licensed under the New BSD license; see the LICENSE file for details.

from xml.sax import make_parser
from xml.sax import ContentHandler

class ServerLister(ContentHandler):
    '''
    List all servers in the XML file.
    '''
    def __init__(self):
        self.servers = {}

    def startElement(self, name, attrs):
        if name != 'server':
            return
        self.servers[attrs.get('selector')] = attrs.get('name')

    def output(self):
        output = ''
        for key, value in self.servers.iteritems():
            output += "{0} ({1})\n".format(value, key)
        return output.rstrip()

class AreaLister(ContentHandler):
    '''
    List all areas in a server.
    '''
    def __init__(self, server):
        self.find_server = server
        self.areas = []
        self.in_target_server = False # was the last <server> tag we saw
                                      # the one we are interested in?

    def startElement(self, name, attrs):
        '''
        We are interested in <server> tags and <area> tags.
        If we find the <server> tag for the server we want, set a flag.
        If the flag is on and we find an <area> tag, add it to the list.
        '''
        if name == 'server' and attrs.get('selector') == self.find_server:
            self.in_target_server = True
            return

        if name == 'area' and self.in_target_server:
            self.areas.append(attrs.get('selector'))

    def endElement(self, name):
        '''
        If we found a </server> tag, and the last <server> tag was the one
        we were looking for, we are all done.
        '''
        if self.in_target_server and name == 'server':
            self.in_target_server = False

    def output(self):
        output = ''
        for area in self.areas:
            output += "{0}\n".format(area)
        return output.rstrip()

class DataLister(ContentHandler):
    '''
    List a piece of data for a server/area combo.
    '''
    def __init__(self, server, area, key):
        self.find_server, self.find_area, self.find_key = server, area, key
        self.in_target_server = False
        self.in_target_area   = False
        self.in_target_key    = False
        self.data = ''

    def startElement(self, name, attrs):
        '''
        Keep flags set if we are in the right server and area.
        The data tag we are looking for changes based on passed args.
        '''
        if name == 'server' and attrs.get('selector') == self.find_server:
            self.in_target_server = True
            return

        if self.in_target_server and name == 'area' and attrs.get('selector') == self.find_area:
            self.in_target_area = True
            return

        if self.in_target_area and name == self.find_key:
            self.in_target_key = True
            return

    def endElement(self, name):
        if self.in_target_key and name == self.find_key:
            self.in_target_key = False
            return

        if self.in_target_area and name == 'area':
            self.in_target_area = False
            return

        if self.in_target_server and name == 'server':
            self.in_target_server = False
            return

    def characters(self, ch):
        if self.in_target_key:
            self.data += ch

    def output(self):
        return "{0}\n".format(self.data).rstrip()
