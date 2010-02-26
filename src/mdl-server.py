#!/usr/bin/env python

# Copyright (c) 2010, Fresno Pacific University
# Licensed under the New BSD license; see the LICENSE file for details.

from MoodleTools.MdlServer import MdlServer
from MoodleTools.Exceptions import *
import sys

err = sys.stderr

# ==============================================================================
# Execute the program
# ==============================================================================
try:
    mdl_svr = MdlServer()
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
