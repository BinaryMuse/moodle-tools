#!/usr/bin/env python

# Copyright (c) 2010, Fresno Pacific University
# Licensed under the New BSD license; see the LICENSE file for details.

import os, sys, shutil, unittest
from mock import Mock
from optparse import Values
from MoodleTools.mdl_server import mdl_server
from BeQuiet import *

class test_mdl_server(unittest.TestCase):
    def setUp(self):
        self.xml_file = 'test/test_mdl-server.xml'
        self.envs = {}

        self.command = mdl_server()
        self.command.parseOptions = Mock()
        self.command.parseOptions.side_effect = self.mock_parseOptions()

    def mock_parseOptions(self):
        self.command.options = Values()
        self.command.options.file = self.xml_file
        self.command.args = []

    def save_env(self, var):
        '''
        Save the environment variable var in the has table;
        save it as default if it does not exist.
        '''
        oldenviron = None
        try:
            oldenviron = os.environ['MDL_SERVER_CONFIG']
        except KeyError:
            pass
        self.envs[var] = oldenviron

    def restore_env(self, var):
        '''
        Restore the environment variable var from the hash table
        unless it has the value unless.
        '''
        savedenv = None
        try:
            savedenv = self.envs[var]
        except KeyError:
            return
        if not savedenv == None:
            os.environ[var] = savedenv

    # ==========================================================================
    # Testing mdl_server.main()
    # ==========================================================================

    def test_too_many_args_return_code(self):
        '''
        Too many args on command line should result in a non-zero exit code
        '''
        self.command.args = ['a', 'b', 'c', 'd']
        with BeQuiet():
            self.assertNotEqual(self.command.main(), 0)

    def test_bad_file_return_code(self):
        '''
        File-not-found error should result in a non-zero exit code
        '''
        self.command.options.file = 'boogieboogie.asdf'
        with BeQuiet():
            self.assertNotEqual(self.command.main(), 0)

    def test_bad_arguments_return_code(self):
        '''
        A bad list of arguments should result in a non-zero exit code
        '''
        self.command.args = ['prod', 'fake', 'wheeee']
        with BeQuiet():
            self.assertNotEqual(self.command.main(), 0)

    # ==========================================================================
    # Testing mdl_server.parseOptions()
    # ==========================================================================

    def test_argument_file_found(self):
        '''
        Passing a good file should result in that file being used
        '''
        self.command.chooseConfigFile()
        self.assertEqual(self.command.options.file, self.xml_file)

    def test_argument_file_not_found(self):
        '''
        Passing a bad file should result in empty string even if env is set
        '''
        self.save_env('MDL_SERVER_CONFIG')
        os.environ['MDL_SERVER_CONFIG'] = os.getcwd() + '/' + self.xml_file
        self.command.options.file = 'fakefileisfake.bigphoney';
        self.command.chooseConfigFile()
        self.assertEqual(self.command.options.file, '')
        self.restore_env('MDL_SERVER_CONFIG')

    def test_argument_file_blank_use_env(self):
        '''
        Passing no file should result in using env if set
        '''
        self.save_env('MDL_SERVER_CONFIG')
        filetouse = os.getcwd() + '/test/test_mdl-server.xml'
        os.environ['MDL_SERVER_CONFIG'] = filetouse
        self.command.options.file = ''
        self.command.chooseConfigFile()
        self.assertEqual(self.command.options.file, filetouse)
        self.restore_env('MDL_SERVER_CONFIG')

    def test_argument_file_blank_env_bad(self):
        '''
        Passing no file and having a bad env should result in empty string
        '''
        self.save_env('MDL_SERVER_CONFIG')
        os.environ['MDL_SERVER_CONFIG'] = "fakefile.bigphoney"
        self.command.options.file = ''
        self.command.chooseConfigFile()
        self.assertEqual(self.command.options.file, '')
        self.restore_env('MDL_SERVER_CONFIG')

    def test_argument_file_blank_no_env_use_cwd(self):
        '''
        Passing no file and having no env should use mdl-server.xml in cwd
        '''
        self.save_env('MDL_SERVER_CONFIG')
        try:
            del os.environ['MDL_SERVER_CONFIG']
        except KeyError:
            pass
        olddir = os.getcwd()
        os.chdir('test')
        # Assert last so all the file moves can be done even if the test fails
        shutil.move('test_mdl-server.xml', 'mdl-server.xml')
        self.command.options.file = ''
        self.command.chooseConfigFile()
        shutil.move('mdl-server.xml', 'test_mdl-server.xml')
        os.chdir('..')
        self.restore_env('MDL_SERVER_CONFIG')
        self.assertEqual(self.command.options.file, olddir + '/test/mdl-server.xml')

    # ==========================================================================
    # Testing mdl_server.parseXml()
    # ==========================================================================

    def test_server_list(self):
        '''
        Test that the list of servers is correct
        '''
        with BeQuiet():
            self.command.main()
        expected = "Test Moodle Server (test)\nProduction Moodle Server (prod)"
        self.assertEqual(self.command.output, expected)

    def test_area_list(self):
        '''
        Test that the list of areas is correct
        '''
        with BeQuiet():
            self.command.args = ['prod']
            self.command.main()
        expected = "live\nstage"
        self.assertEqual(self.command.output, expected)

    def test_data_list(self):
        '''
        Test that the list of areas is correct
        '''
        with BeQuiet():
            self.command.args = ['prod', 'live']
            self.command.main()
        expected = "/Volumes/moodle3-e/moodle"
        self.assertEqual(self.command.output, expected)

    def test_data_list_specific(self):
        '''
        Test that the list of areas is correct
        '''
        with BeQuiet():
            self.command.args = ['test', 'stage', 'data']
            self.command.main()
        expected = "/Volumes/moodle2-e/moodleuploads"
        self.assertEqual(self.command.output, expected)
