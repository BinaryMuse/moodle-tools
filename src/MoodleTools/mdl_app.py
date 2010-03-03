#!/usr/bin/env python

# Copyright (c) 2010, Fresno Pacific University
# Licensed under the New BSD license; see the LICENSE file for details.

import os

class mdl_app:
    '''
    Parent of all mdl_* application classes.
    Defines common functionality.
    '''
    def get_exec_path(self):
        path = ''
        try:
            path = os.environ['MDL_TOOLS_EXEC_PATH']
        except KeyError:
            pass

        return path