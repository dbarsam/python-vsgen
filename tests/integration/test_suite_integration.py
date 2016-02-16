# -*- coding: utf-8 -*-
"""
This module provides all integration test for the suite functionality.
"""
import os
import unittest
import shutil
import logging

from vsgen import __main__


def setUpModule():
    """
    The module specific setUp method
    """
    logging.disable(logging.CRITICAL)


def tearDownModule():
    """
    The module specific tearDown method
    """
    logging.disable(logging.NOTSET)


class TestIntegrationConfigurationFile(unittest.TestCase):
    """
    Tests the Solution and Project Generation from a cofiguration file.
    """

    def setUp(self):
        """
        The class specific setUp method
        """
        self._data = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'data'))
        self.assertTrue(os.path.isdir(self._data), 'Test data directory "{}" does not exist'.format(self._data))

        self._output = os.path.normpath(os.path.join(self._data, '_output'))
        self.assertFalse(os.path.exists(self._output), 'Test output directory already exits!'.format(self._output))

        self._file = os.path.normpath(os.path.join(self._data, 'vsgencfg', 'setup.cfg'))
        self.assertTrue(os.path.isfile(self._file), 'Test configuration file "{}" does not exist'.format(self._file))

    def tearDown(self):
        """
        The class specific tearDown method
        """
        # Remove the output directory
        if os.path.exists(self._output):
            shutil.rmtree(self._output)

    def test_configuration_file_success(self):
        """
        Tests the expected workflow.
        """
        result = __main__.main([__main__.__file__, self._file])
        self.assertEqual(result, 0)

if __name__ == '__main__':
    unittest.main()
