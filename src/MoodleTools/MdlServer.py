#!/usr/bin/env python

from optparse import OptionParser
from xml.dom import minidom
from MoodleTools.Exceptions import *

# ==============================================================================
# Define the application class
# ==============================================================================
class MdlServer:
    def __init__(self):
        """Initialize data and wait for the calling program to issue instructions."""
        self.data = {}

    def go(self):
        """Start 'er up."""
        self.parseOptions()
        self.parse()
        self.executeByArgs()

    def parseOptions(self):
        """Parse options passed to the script via the command line."""
        parser = OptionParser(usage="%prog [options] [<server> [<area> [<data>]]]",
            description="Outputs configuration data. Specify a server, a server and an area, or a server, " +
            "area, and data element (src or data) to print appropriate data.", version="Moodle Tools mdl-server 0.1")
        parser.add_option("-f", "--file", metavar="FILE", help="use FILE instead of mdl-server.xml", default="mdl_server.xml")

        (self.options, self.args) = parser.parse_args()

    def parse(self):
        """Parse the data in the XML file."""
        self.xml = minidom.parse(self.options.file)
        
        self.servernodes = self.getServerNodes()               # List of server dicts # Dict of server dicts, keyed by selector
                                                               # e.g. servernodes['prod']['name']
        self.areanodes   = self.getAreaNodes(self.servernodes) # Dict of area lists
                                                               # e.g. areanodes['prod']['live']['selector']
        self.datanodes   = self.getDataNodes(self.areanodes)   # Multidimensional dict defining data for sever-area combos
                                                               # e.g. datanodes['prod']['stage']['src']

    def executeByArgs(self):
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
        retval = ''
        for svr_selector, svr_data in self.servernodes.iteritems():
            retval += "{0} ({1})\n".format(svr_data['name'], svr_selector)
        return retval.rstrip()

    def listAreas(self, server):
        if not self.areanodes.has_key(server):
            raise ServerNotFoundError(server)

        retval = ''
        for area_selector, area_data in self.areanodes[server].iteritems():
            retval += '{0}\n'.format(area_selector)
        return retval.rstrip()

    def listData(self, server, area, data):
        if not self.datanodes.has_key(server):
            raise ServerNotFoundError(server)
        if not self.datanodes[server].has_key(area):
            raise AreaNotFoundError(area)
        if not self.datanodes[server][area].has_key(data):
            raise InvalidDataKeyError(data)

        return self.datanodes[server][area][data]

    def getServerNodes(self):
        """Return a list of dicts defining each dictionary"""
        servernodes = {}
        for svrnode in self.xml.getElementsByTagName('server'):
            name = svrnode.getAttribute('name')
            selector = svrnode.getAttribute('selector')
            servernodes[selector] = {'node': svrnode, 'name': name, 'selector': selector}
        return servernodes

    def getAreaNodes(self, servernodes):
        """Return a dict of (server-selector: area-list) pairs,
        where area-list is a list of dicts"""
        areanodes = {}
        for svrselector, svrentry in servernodes.iteritems():
            node = svrentry['node']
            areas = {}
            for areanode in node.getElementsByTagName('area'):
                selector = areanode.getAttribute('selector')
                areas[selector] = {'node': areanode, 'selector': selector}
            areanodes[svrselector] = areas
        return areanodes

    def getDataNodes(self, areanodes):
        """Return a dict in the following format:
          svr_dict  area_dict        data_dict
        { server: { area selector: { src: src-path, data: data-path},
                    area selector: { src: src-path, data: data-path}
                  },
          server: ... }"""
        svr_data = {}
        # Iterate over the areanodes dict
        for svr_selector, area_dict in areanodes.iteritems():
            area_data = {}
            for area_selector, area_data_dict in area_dict.iteritems():
                data_data = {}
                src_nodes = area_data_dict['node'].getElementsByTagName('src')
                src = src_nodes[0].firstChild.data
                data_nodes = area_data_dict['node'].getElementsByTagName('data')
                data = data_nodes[0].firstChild.data
                data_data['src'] = src
                data_data['data'] = data
                area_data[area_selector] = data_data
            svr_data[svr_selector] = area_data
        return svr_data
