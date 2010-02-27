#!/usr/bin/env python

# Copyright (c) 2010, Fresno Pacific University
# Licensed under the New BSD license; see the LICENSE file for details.

import sys
from optparse import OptionParser
from MoodleTools.MdlServer import MdlServer
from MoodleTools.Exceptions import *

err = sys.stderr

# ==============================================================================
# Parse options
# ==============================================================================

parser = OptionParser(usage="%prog [options] [<server> [<area> [<data>]]]",
    description="Outputs configuration data. Specify a server, a server and an area, or a server, " +
    "area, and data element (src or data) to print appropriate data.", version="Moodle Tools mdl-server 0.1")
parser.add_option("-f", "--file", metavar="FILE", help="use FILE instead of mdl-server.xml", default="mdl_server.xml")

(options, args) = parser.parse_args()

# ==============================================================================
# Execute the program
# ==============================================================================
try:
    mdl_svr = MdlServer(options, args)
    mdl_svr.go()
except IOError as (errorno, errorstr):
    print >> err, "{0} was not found. See the --file option if you want to parse another XML file.".format(errorstr)
    quit(1)
except TooManyArgsError:
    print >> err, "Too many parameters passed."
    quit(1)
except ServerNotFoundError as e:
    print >> err, "The server '{0}' was not found in the XML file.".format(e)
    quit(1)
except AreaNotFoundError as e:
    print >> err, "The area '{0}' was not found in the XML file.".format(e)
    quit(1)
except InvalidDataKeyError as e:
    print >> err, "The data key '{0}' was not found in the XML file.".format(e)
    quit(1)

quit(0)
