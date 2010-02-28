#!/usr/bin/env python

# Copyright (c) 2010, Fresno Pacific University
# Licensed under the New BSD license; see the LICENSE file for details.

import os
import shutil
import sys
import StringIO
import unittest
from optparse import Values
from MoodleTools.MdlServer import MdlServer
from MoodleTools.Exceptions import *

class test_MdlServer(unittest.TestCase):
    def setUp(self):
        '''
        Set up some default arguments.
        '''
        options = Values()
        options.file = 'test/test_mdl-server.xml'
        args = []
        self.mdlsrv = MdlServer(options, args)

    def testFileNotFoundNoEnv(self):
        '''
        Test that an incorrect XML file generates exception if the env is not set.
        '''
        oldenviron = None
        try:
            oldenviron = os.environ['MDL_SERVER_CONFIG']
        except KeyError:
            pass
        else:
            del(os.environ['MDL_SERVER_CONFIG'])
        self.mdlsrv.options.file = "notfound.xml"
        self.assertRaises(IOError, self.mdlsrv.parse)
        if(not oldenviron == None):
            os.environ['MDL_SERVER_CONFIG'] = oldenviron

    def textFileNotFoundWithEnv(self):
        '''
        Test that an incorrect XML file generates exception even if env is set.
        '''
        oldenviron = None
        try:
            oldenviron = os.environ['MDL_SERVER_CONFIG']
        except KeyError:
            pass
        os.environ['MDL_SERVER_CONFIG'] = os.getcwd() + '/test/test_mdl-server.xml'
        self.mdlsrv.options.file = "notfound.xml"
        self.assertRaises(IOError, self.mdlsrv.parse)
        if(not oldenviron == None):
            os.environ['MDL_SERVER_CONFIG'] = oldenviron

    def testFileNotPassedUseEnviron(self):
        '''
        Test that not specifying a file with good env set will use env.
        '''
        oldenviron = None
        try:
            oldenviron = os.environ['MDL_SERVER_CONFIG']
        except KeyError:
            pass
        os.environ['MDL_SERVER_CONFIG'] = os.getcwd() + '/test/test_mdl-server.xml'
        self.mdlsrv.options.file = ''
        self.mdlsrv.parse()
        servers = self.mdlsrv.servernodes.keys()
        self.assertEqual(len(servers), 2)
        self.assertTrue('prod' in servers)
        self.assertTrue('test' in servers)
        if(not oldenviron == None):
            os.environ['MDL_SERVER_CONFIG'] = oldenviron

    def testFileNotPassedNoEnvironNoCwd(self):
        '''
        Test that not specifying a file and not using env gives an error if mdl-server.xml not found.
        '''
        oldenviron = None
        try:
            oldenviron = os.environ['MDL_SERVER_CONFIG']
        except KeyError:
            pass
        else:
            del os.environ['MDL_SERVER_CONFIG']
        self.mdlsrv.options.file = ""
        self.assertRaises(IOError, self.mdlsrv.parse)
        if(not oldenviron == None):
            os.environ['MDL_SERVER_CONFIG'] = oldenviron

    def testFileNotPassedNoEnvironUseCwd(self):
        '''
        Test that not specifying a file and not using env uses mdl-server.xml if found.
        '''
        oldenviron = None
        try:
            oldenviron = os.environ['MDL_SERVER_CONFIG']
        except KeyError:
            pass
        else:
            del os.environ['MDL_SERVER_CONFIG']
        self.mdlsrv.options.file = ''
        olddir = os.getcwd()
        os.chdir('test')
        shutil.move('test_mdl-server.xml', 'mdl-server.xml')
        print os.getcwd()
        self.mdlsrv.parse()
        shutil.move('mdl-server.xml', 'test_mdl-server.xml')
        os.chdir('..')
        if(not oldenviron == None):
            os.environ['MDL_SERVER_CONFIG'] = oldenviron

    def testCorrectServers(self):
        '''
        Test that the class returns the correct servers from the XML file.
        '''
        self.mdlsrv.parse()
        servers = self.mdlsrv.servernodes.keys()
        self.assertEqual(len(servers), 2)
        self.assertTrue('prod' in servers)
        self.assertTrue('test' in servers)

    def testCorrectServerNames(self):
        '''
        Test that the class associates the right server names with the selectors.
        '''
        self.mdlsrv.parse()
        nodes = self.mdlsrv.servernodes
        self.assertEqual(nodes['prod']['name'], 'Production Moodle Server')
        self.assertEqual(nodes['test']['name'], 'Test Moodle Server')

    def testCorrectAreas(self):
        '''
        Test that the class returns the correct areas for a given server.
        '''
        self.mdlsrv.parse()
        areas = self.mdlsrv.areanodes['prod'].keys()
        self.assertEqual(len(areas), 2)
        self.assertTrue('live' in areas)
        self.assertTrue('stage' in areas)

    def testCorrectData(self):
        '''
        Test that the correct path data can be retrieved from the class.
        '''
        self.mdlsrv.parse()
        src = self.mdlsrv.datanodes['prod']['live']['src']
        data = self.mdlsrv.datanodes['test']['stage']['data']
        self.assertEqual(src, '/Volumes/moodle3-e/moodle')
        self.assertEqual(data, '/Volumes/moodle2-e/moodleuploads')

    def testCorrectOutputServer(self):
        '''
        Test that the output of the program is as expected when passed no arguments.
        '''
        oldstdout = sys.stdout
        capture = StringIO.StringIO()
        sys.stdout = capture
        self.mdlsrv.go()
        sys.stdout = oldstdout
        print capture.getvalue()
        self.assertEqual(capture.getvalue(), "Test Moodle Server (test)\nProduction Moodle Server (prod)\n")

    def testCorrectOutputArea(self):
        '''
        Test that the output of the program is as expected when passed a server.
        '''
        oldstdout = sys.stdout
        capture = StringIO.StringIO()
        sys.stdout = capture
        self.mdlsrv.args = ['prod']
        self.mdlsrv.go()
        sys.stdout = oldstdout
        print capture.getvalue()
        self.assertEqual(capture.getvalue(), "live\nstage\n")

    def testCorrectOutputData(self):
        '''
        Test that the output of the program is as expected when passed a server and an area.
        '''
        oldstdout = sys.stdout
        capture = StringIO.StringIO()
        sys.stdout = capture
        self.mdlsrv.args = ['prod', 'live']
        self.mdlsrv.go()
        sys.stdout = oldstdout
        print capture.getvalue()
        self.assertEqual(capture.getvalue(), "/Volumes/moodle3-e/moodle\n")

    def testCorrectOutputDataSpecific(self):
        '''
        Test that the output of the program is as expected when passed a server, area, and data key.
        '''
        oldstdout = sys.stdout
        capture = StringIO.StringIO()
        sys.stdout = capture
        self.mdlsrv.args = ['prod', 'live', 'data']
        self.mdlsrv.go()
        sys.stdout = oldstdout
        print capture.getvalue()
        self.assertEqual(capture.getvalue(), "/Volumes/moodle3-f/moodledata\n")

    def testServerNotFoundException(self):
        '''
        Test that an exception is raised when a server can\'t be found.
        '''
        self.mdlsrv.args = ['fakeserver']
        self.assertRaises(ServerNotFoundError, self.mdlsrv.go)
        self.mdlsrv.args = ['fakeserver', 'fakearea']
        self.assertRaises(ServerNotFoundError, self.mdlsrv.go)

    def testAreaNotFoundException(self):
        '''
        Test that an exception is raised when an area can\'t be found.
        '''
        self.mdlsrv.args = ['prod', 'fakearea']
        self.assertRaises(AreaNotFoundError, self.mdlsrv.go)

    def testInvalidDataKeyException(self):
        '''
        Test that an exception is raised when a server can\'t be found.
        '''
        self.mdlsrv.args = ['prod', 'live', 'fakekey']
        self.assertRaises(InvalidDataKeyError, self.mdlsrv.go)

    def testTooManyArgsException(self):
        '''
        Test that an exception is raised when too many parameters are passed.
        '''
        self.mdlsrv.args = ['prod', 'live', 'data', 'stuff']
        self.assertRaises(TooManyArgsError, self.mdlsrv.go)

if __name__ == '__main__':
    unittest.main()
