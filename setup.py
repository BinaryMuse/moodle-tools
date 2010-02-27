#!/usr/bin/env python

# Copyright (c) 2010, Fresno Pacific University
# Licensed under the New BSD license; see the LICENSE file for details.

from distutils.core import setup

setup(name='moodle-tools',
      version = '0.1a',
      description = 'Tools to help administer Moodle installations',
      author = 'Brandon Tilley',
      author_email = 'brandon.tilley@fresno.edu',
      url = 'http://binarymuse.github.com/moodle-tools',
      packages = ['MoodleTools'],
      package_dir = {'MoodleTools': 'src/MoodleTools'},
      scripts = ['src/mdl-server'],
      license = 'New BSD License'
      )
