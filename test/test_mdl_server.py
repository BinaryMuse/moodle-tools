#!/usr/bin/env python

# Copyright (c) 2010, Fresno Pacific University
# Licensed under the New BSD license; see the LICENSE file for details.

import os
import unittest
import shutil
from MoodleTools.mdl_server import *

class test_MdlServer_Driver(unittest.TestCase):
    def setUp(self):
        self.filename = 'test/test_mdl-server.xml'

    # ==========================================================================
    # Testing mdl_server.chooseConfigFile()
    # ==========================================================================

    def testConfigFile_ValidFromCommandLine(self):
        '''
        Good file passed on command line; should return that file name
        '''
        self.assertEqual(chooseConfigFile(self.filename), self.filename)

    def testConfigFile_InvalidFromCommandLine_GoodEnviron(self):
        '''
        Bad file passed on command line; good env; should return empty string
        '''
        oldenviron = None
        try:
            oldenviron = os.environ['MDL_SERVER_CONFIG']
        except KeyError:
            pass
        os.environ['MDL_SERVER_CONFIG'] = os.getcwd() + '/test/test_mdl-server.xml'
        self.assertEqual(chooseConfigFile('fakefileisfake.fake'), '')
        if(not oldenviron == None):
            os.environ['MDL_SERVER_CONFIG'] = oldenviron

    def testConfigFile_NoneFromCommandLine_GoodEnviron(self):
        '''
        No file passed on command line; good env; should return MDL_SERVER_CONFIG
        '''
        oldenviron = None
        try:
            oldenviron = os.environ['MDL_SERVER_CONFIG']
        except KeyError:
            pass
        os.environ['MDL_SERVER_CONFIG'] = os.getcwd() + '/test/test_mdl-server.xml'
        self.assertEqual(chooseConfigFile(''), os.environ['MDL_SERVER_CONFIG'])
        if(not oldenviron == None):
            os.environ['MDL_SERVER_CONFIG'] = oldenviron

    def testConfigFile_NoneFromCommandLine_NoEnviron(self):
        '''
        No file passed on command line; no env; should return empty string
        '''
        oldenviron = None
        try:
            oldenviron = os.environ['MDL_SERVER_CONFIG']
        except KeyError:
            pass
        else:
            del os.environ['MDL_SERVER_CONFIG']
        self.assertEqual(chooseConfigFile(''), '')
        if(not oldenviron == None):
            os.environ['MDL_SERVER_CONFIG'] = oldenviron

    def testConfigFile_NoneFromCommandLine_NoEnviron_UseCwd(self):
        '''
        Test that not specifying a file and not using env uses mdl-server.xml if found
        '''
        oldenviron = None
        try:
            oldenviron = os.environ['MDL_SERVER_CONFIG']
        except KeyError:
            pass
        else:
            del os.environ['MDL_SERVER_CONFIG']
        olddir = os.getcwd()
        os.chdir('test')
        # Capture the output before asserting so that the file gets put
        # back even if the test fails
        shutil.move('test_mdl-server.xml', 'mdl-server.xml')
        output = chooseConfigFile('')
        shutil.move('mdl-server.xml', 'test_mdl-server.xml')
        os.chdir('..')
        if(not oldenviron == None):
            os.environ['MDL_SERVER_CONFIG'] = oldenviron
        self.assertEqual(output, olddir + '/test/mdl-server.xml')

    # ==========================================================================
    # Testing mdl_server.parseXml()
    # ==========================================================================

    def testServerList(self):
        '''
        Test that the list of servers is correct
        '''
        output = parseXml(self.filename, [])
        self.assertEqual(output, "Test Moodle Server (test)\nProduction Moodle Server (prod)")

    def testAreaList(self):
        '''
        Test that the list of areas is correct
        '''
        output = parseXml(self.filename, ['prod'])
        self.assertEqual(output, "live\nstage")

    def testData(self):
        '''
        Test that the data is correct with no key argument
        '''
        output = parseXml(self.filename, ['prod', 'live'])
        self.assertEqual(output, "/Volumes/moodle3-e/moodle")

    def testDataSpecified(self):
        '''
        Test that the data is correct with a key argument
        '''
        output = parseXml(self.filename, ['test', 'stage', 'data'])
        self.assertEqual(output, "/Volumes/moodle2-e/moodleuploads")

if __name__ == '__main__':
    unittest.main()