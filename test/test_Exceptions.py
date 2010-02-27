#!/usr/bin/env python

import unittest
from MoodleTools.Exceptions import *

class test_Exceptions(unittest.TestCase):
    def setUp(self):
        pass

    def testServerNotFoundError(self):
        try:
            raise ServerNotFoundError('myTestServer')
        except ServerNotFoundError as exc:
            self.assertEqual(str(exc), 'myTestServer')

    def testAreaNotFoundError(self):
        try:
            raise AreaNotFoundError('myTestArea')
        except AreaNotFoundError as exc:
            self.assertEqual(str(exc), 'myTestArea')

    def testInvalidDataKeyError(self):
        try:
            raise InvalidDataKeyError('myTestDataKey')
        except InvalidDataKeyError as exc:
            self.assertEqual(str(exc), 'myTestDataKey')

if __name__ == '__main__':
    unittest.main()
