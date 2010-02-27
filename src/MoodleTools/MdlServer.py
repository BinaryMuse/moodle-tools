#!/usr/bin/env python

# Copyright (c) 2010, Fresno Pacific University
# Licensed under the New BSD license; see the LICENSE file for details.

import os
from xml.dom import minidom
from MoodleTools.Exceptions import *

# ==============================================================================
# Define the application class
# ==============================================================================
class MdlServer:
    def __init__(self, options, args):
        '''
        Initialize data and wait for the calling program to issue instructions.
        options and args passed from calling program, generated from OptionParser
        '''
        self.options, self.args = options, args
        self.data = {}

    def go(self):
        '''
        Start 'er up.
        '''
        self.parse()
        self.executeByArgs()

    def parse(self):
        '''
        Parse the data in the XML file.
        Each dictionary contains attributes called 'node'. The data referenced
        contains the actual minidom objects we can iterate over.
        '''
        # If we can't find the file specified, check on the MDL_SERVER_CONFIG
        # environment variable.
        filename = self.options.file
        if(not os.path.isfile(filename)):
            filename = os.environ['MDL_SERVER_CONFIG']
        self.xml = minidom.parse(os.path.expanduser(filename))

        self.servernodes = self.getServerNodes()               # List of server dicts # Dict of server dicts, keyed by selector
                                                               # e.g. servernodes['prod']['name']
        self.areanodes   = self.getAreaNodes(self.servernodes) # Dict of area lists
                                                               # e.g. areanodes['prod']['live']['selector']
        self.datanodes   = self.getDataNodes(self.areanodes)   # Multidimensional dict defining data for sever-area combos
                                                               # e.g. datanodes['prod']['stage']['src']

    def executeByArgs(self):
        '''
        Output the requested data by counting command line arguments.
        '''
        args = self.args
        if len(args) == 0:
            print self.listServers()
        elif len(args) == 1:
            print self.listAreas(args[0])
        elif len(args) == 2:
            print self.listData(args[0], args[1], 'src')
        elif len(args) == 3:
            print self.listData(args[0], args[1], args[2])
        else:
            raise TooManyArgsError

    def listServers(self):
        '''
        Output a list of the servers.
        '''
        retval = ''
        for svr_selector, svr_data in self.servernodes.iteritems():
            retval += "{0} ({1})\n".format(svr_data['name'], svr_selector)
        return retval.rstrip()

    def listAreas(self, server):
        '''
        Output a list of the areas for a server.
        '''
        if not self.areanodes.has_key(server):
            raise ServerNotFoundError(server)

        retval = ''
        for area_selector, area_data in self.areanodes[server].iteritems():
            retval += '{0}\n'.format(area_selector)
        return retval.rstrip()

    def listData(self, server, area, data):
        '''
        Output a specific piece of data for a server/area combo.
        '''
        if not self.datanodes.has_key(server):
            raise ServerNotFoundError(server)
        if not self.datanodes[server].has_key(area):
            raise AreaNotFoundError(area)
        if not self.datanodes[server][area].has_key(data):
            raise InvalidDataKeyError(data)

        return self.datanodes[server][area][data]

    def getServerNodes(self):
        '''
        Searches the XML for the servers and returns a dictionary.
        '''
        servernodes = {}
        for svrnode in self.xml.getElementsByTagName('server'):
            name = svrnode.getAttribute('name')
            selector = svrnode.getAttribute('selector')
            servernodes[selector] = {'node': svrnode, 'name': name, 'selector': selector}
        return servernodes

    def getAreaNodes(self, servernodes):
        '''
        Searches through the XML for the areas and returns a dictionary.
        '''
        areanodes = {}
        for svrselector, svrentry in servernodes.iteritems():
            # The 'node' attribute has the actual minidom objects
            node = svrentry['node']
            areas = {}
            for areanode in node.getElementsByTagName('area'):
                selector = areanode.getAttribute('selector')
                areas[selector] = {'node': areanode, 'selector': selector}
            areanodes[svrselector] = areas
        return areanodes

    def getDataNodes(self, areanodes):
        '''
        Searches the XML for the data for an area and returns a dictionary.
        '''
        svr_data = {}
        # Iterate over the areanodes dict
        for svr_selector, area_dict in areanodes.iteritems():
            area_data = {}
            for area_selector, area_data_dict in area_dict.iteritems():
                data_data = {}
                # The 'node' attribute has the actual minidom objects
                src_nodes = area_data_dict['node'].getElementsByTagName('src')
                src = src_nodes[0].firstChild.data
                data_nodes = area_data_dict['node'].getElementsByTagName('data')
                data = data_nodes[0].firstChild.data
                data_data['src'] = src
                data_data['data'] = data
                area_data[area_selector] = data_data
            svr_data[svr_selector] = area_data
        return svr_data
