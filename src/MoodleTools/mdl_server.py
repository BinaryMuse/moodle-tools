#!/usr/bin/env python

# Copyright (c) 2010, Fresno Pacific University
# Licensed under the New BSD license; see the LICENSE file for details.

import os, sys
from os.path import abspath, expanduser
from optparse import OptionParser
from MoodleTools.ServerConfigParser import *

class mdl_server:
    '''
    Application class for mdl-server
    '''
    def __init__(self):
        pass # nothing to do

    def main(self):
        '''
        Run the application. This method should return return_code.
        01: Configuration file could not be found
        02: Too many arguments were passed
        03: parseXml() could not find the specified data
        '''
        # If no data key is passed, we assume one.
        self.DEFAULT_DATA_KEY = 'src'

        self.parseOptions()
        self.chooseConfigFile()
        # Exit with an error if no configuration file could be found.
        if self.options.file == '' or self.options.file == None:
            print >> sys.stderr, "Could not find a configuration file.",
            print >> sys.stderr, "See the --help option for details on",
            print >> sys.stderr, "specifying a file."
            return 1

        # Check our arguments length.
        if len(self.args) > 3:
            print >> sys.stderr, "Too many arguments passed."
            return 2

        # Do the magic.
        self.parseXml()
        if self.output == None or self.output.strip() == '':
            print >> sys.stderr, "Couldn't find what you were looking for."
            return 3
        else:
            print self.output
            return 0

    def parseOptions(self):
        '''
        Parse out command line options.
        '''
        parser = OptionParser(
            usage = "%prog [options] [SERVER [AREA [DATA]]]",
            description = "Outputs configuration data. Specify a server, a " +
                "server and an area, or a server, area, and data element (src or "+
                " data) to print appropriate data."
        )
        parser.add_option(
            "-f", "--file",
            metavar = "FILE",
            help = "use FILE instead of MDL_SERVER_CONFIG or mdl-server.xml",
            default = ''
        )

        self.options, self.args = parser.parse_args()

    def chooseConfigFile(self):
        '''
        Pick a file to parse based on the following rules:
        If -f or --file was passed and the file exists, use that.
        If -f or --file was not used, and MDL_SERVER_CONFIG is set and exists,
            use that.
        If neither -f/--file or MDL_SERVER_CONFIG is valid, look for mdl-server.xml
            in the current working directory.
        '''
        # See if -f/--file is valid.
        if os.path.isfile(abspath(expanduser(self.options.file))):
            return

        # If -f/--file was indeed used, and the file doesn't exist, don't fall
        # through; instead, return '' so error handling can take care of it.
        if not self.options.file == '':
            self.options.file = ''
            return

        # The file passed wasn't valid; check the environment.
        try:
            self.options.file = abspath(expanduser(os.environ['MDL_SERVER_CONFIG']))
        except KeyError:
            self.options.file = ''
        if os.path.isfile(abspath(self.options.file)):
            return

        # The environment wasn't valid or not set. Check the cwd.
        self.options.file = os.getcwd() + '/mdl-server.xml'
        if os.path.isfile(abspath(self.options.file)):
            return

        # Nothing; return and let the error handling take care of it.
        self.options.file = ''

    def parseXml(self):
        '''
        Determine what should be outputted based on args and parse out the XML
        accordingly.
        '''
        parser = make_parser()
        handler = None
        if len(self.args) == 0:
            handler = ServerLister()
        elif len(self.args) == 1:
            handler = AreaLister(self.args[0])
        elif len(self.args) == 2:
            key = self.DEFAULT_DATA_KEY
            handler = DataLister(self.args[0], self.args[1], key)
        elif len(self.args) == 3:
            handler = DataLister(self.args[0], self.args[1], self.args[2])

        if not handler == None:
            parser.setContentHandler(handler)
            parser.parse(self.options.file)
            self.output = handler.output()
