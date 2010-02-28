#!/usr/bin/env python

# Copyright (c) 2010, Fresno Pacific University
# Licensed under the New BSD license; see the LICENSE file for details.

import os
from optparse import OptionParser
from MoodleTools.ServerConfigParser import *

def parseOptions():
    '''
    Parse out command line options.
    '''
    parser = OptionParser(
        usage = "%prog [options] [<server> [<area> [<data>]]]",
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

    (options, args) = parser.parse_args()
    return options, args

def chooseConfigFile(filename):
    '''
    Pick a file to parse based on the following rules:
    If -f or --file was passed and the file exists, use that.
    If -f or --file was not used, and MDL_SERVER_CONFIG is set and exists,
        use that.
    If neither -f/--file or MDL_SERVER_CONFIG is valid, look for mdl-server.xml
        in the current working directory.
    '''
    # See if -f/--file is valid.
    if os.path.isfile(os.path.expanduser(filename)):
        return filename

    # If -f/--file was indeed used, and the file doesn't exist, don't fall
    # through; instead, return None so error handling can take care of it.
    if not filename == '':
        return ''

    # The file passed wasn't valid; check the environment.
    try:
        filename = os.path.expanduser(os.environ['MDL_SERVER_CONFIG'])
    except KeyError:
        filename = ''
    if os.path.isfile(filename):
        return filename

    # The environment wasn't valid or not set. Check the cwd.
    filename = os.getcwd() + '/mdl-server.xml'
    if os.path.isfile(filename):
        return filename

    # Nothing; return and let the error handling take care of it.
    return ''

def parseXml(filename, args):
    '''
    Determine what should be outputted based on args and parse out the XML
    accordingly.
    '''
    parser = make_parser()
    handler = None
    if len(args) == 0:
        handler = ServerLister()
    elif len(args) == 1:
        handler = AreaLister(args[0])
    elif len(args) == 2:
        key = 'src'
        handler = DataLister(args[0], args[1], key)
    elif len(args) == 3:
        handler = DataLister(args[0], args[1], args[2])

    if not handler == None:
        parser.setContentHandler(handler)
        parser.parse(filename)
        return handler.output()
