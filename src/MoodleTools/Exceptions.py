#!/usr/bin/env python

# Copyright (c) 2010, Fresno Pacific University
# Licensed under the New BSD license; see the LICENSE file for details.

class TooManyArgsError(Exception):
    pass

class ServerNotFoundError(Exception):
    def __init__(self, server):
        self.server = server
    def __str__(self):
        return self.server

class AreaNotFoundError(Exception):
    def __init__(self, area):
        self.area = area
    def __str__(self):
        return self.area

class InvalidDataKeyError(Exception):
    def __init__(self, key):
        self.key = key
    def __str__(self):
        return self.key
