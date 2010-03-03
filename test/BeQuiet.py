#!/usr/bin/env python

# Copyright (c) 2010, Fresno Pacific University
# Licensed under the New BSD license; see the LICENSE file for details.

import sys

# NullWriter defines a dummy file object which does nothing with its output
class NullWriter:
    def write(self, s):
        pass

# BeQuiet allows stderr output to be temporarily suppressed:
#
# with BeQuiet():
#     stuff stuff stuff
class BeQuiet:
    def __enter__(self):
        self.old_stderr = sys.stderr
        sys.stderr = NullWriter()

    def __exit__(self, type, value, traceback):
        sys.stderr = self.old_stderr
