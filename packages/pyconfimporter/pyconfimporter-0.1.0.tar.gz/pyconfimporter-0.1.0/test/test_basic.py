from __future__ import absolute_import, division, print_function, unicode_literals

import os
import unittest

import pyconfimporter


A = 1
B = 2
C = 3
D = None


class TestPyConfImporter(unittest.TestCase):

    def test_pyconfimporter(self):

        path_to_ext_conf = os.path.join(
            os.path.dirname(__file__), 'ext_conf.py')

        # Test basic injection
        pyconfimporter.inject(path_to_ext_conf)

        assert A == -1
        assert D == 4

        # Try injection that doesn't specify required value
        globals()['E'] = pyconfimporter.Required

        with self.assertRaises(pyconfimporter.VarNotDefined) as cm:
            pyconfimporter.inject(path_to_ext_conf)
        assert cm.exception.args[0] == 'Required variable not defined: E'

        # Try a conf that does not exist.
        with self.assertRaises((IOError, OSError)) as cm:
            pyconfimporter.inject('does_not_exist.py')
        assert cm.exception.args[0] == 'Could not find does_not_exist.py'

        # Try a conf that specifies an unknown variable
        path_to_ext_conf2 = os.path.join(
            os.path.dirname(__file__), 'ext_conf2.py')
        with self.assertRaises(pyconfimporter.UnknownVarDefined) as cm:
            pyconfimporter.inject(path_to_ext_conf2)
        assert cm.exception.args[0] == 'Unknown variable defined: F'
