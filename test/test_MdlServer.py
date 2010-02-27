#!/usr/bin/env python

# Copyright (c) 2010, Fresno Pacific University
# Licensed under the New BSD license; see the LICENSE file for details.

import os
import unittest
from optparse import Values
from MoodleTools.MdlServer import MdlServer

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

    def testFileNotFoundUseEnviron(self):
        '''
        Test that not specifying a file with good env set will use env.
        '''
        oldenviron = None
        try:
            oldenviron = os.environ['MDL_SERVER_CONFIG']
        except KeyError:
            pass
        os.environ['MDL_SERVER_CONFIG'] = os.getcwd() + '/test/test_mdl-server.xml'
        print os.environ['MDL_SERVER_CONFIG']
        self.mdlsrv.options.file = ''
        self.mdlsrv.parse()
        servers = self.mdlsrv.servernodes.keys()
        self.assertEqual(len(servers), 2)
        self.assertTrue('prod' in servers)
        self.assertTrue('test' in servers)
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

if __name__ == '__main__':
    unittest.main()
