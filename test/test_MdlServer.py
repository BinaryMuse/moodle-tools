#!/usr/bin/env python

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
        
    def testFileNotFound(self):
        '''
        Test that an incorrect or missing XML file generates an exception.
        '''
        self.mdlsrv.options.file = "notfound.xml"
        self.assertRaises(IOError, self.mdlsrv.parse)
    
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
