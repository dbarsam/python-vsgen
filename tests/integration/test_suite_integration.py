# -*- coding: utf-8 -*-
"""
This module provides all integration test for the suite functionality.
"""
import sys
import os
import unittest
import shutil
import logging
import pkg_resources

from vsgen import __main__


def setUpModule():
    """
    The module specific setUp method
    """
    logging.disable(logging.CRITICAL)

    # Ensure that the Demo Python packages are available
    datadir = os.path.join(os.path.dirname(__file__), '..', 'data')
    if datadir not in sys.path:
        sys.path.append(datadir)
    import vsgendemo

    # Simulate a real external package install by patching setuptools' entry point table with a vsgdemo mock python package.
    demodistribution = pkg_resources.Distribution(os.path.dirname(__main__.__file__), project_name='vsgendemo', version="0.0")
    try:
        demodistribution._ep_map
    except AttributeError:
        demodistribution._ep_map = {}
    demodistribution._ep_map.update({
        'vsgen.suites': {'demo': pkg_resources.EntryPoint('demo', 'vsgendemo.suite', attrs=('VSGDemoSuite',), dist=demodistribution)},
        'vsgen.projects': {'demo': pkg_resources.EntryPoint('demo', 'vsgendemo.projects', attrs=('VSGAutoDemoProject',), dist=demodistribution)}
    })
    pkg_resources.working_set.add(demodistribution, 'demo')

    # Validate the mock entry point
    suite_classes = {ep.name: ep.load() for ep in pkg_resources.iter_entry_points('vsgen.suites')}
    assert 'demo' in suite_classes, 'Entry Point "demo" not in "vsgen.suites" Entry Point collection'
    assert suite_classes['demo'] == vsgendemo.suite.VSGDemoSuite, 'Entry Point "demo" does not resolve to "vsgendemo.suite.VSGSuite"'

    # Validate the mock entry point
    project_classes = {ep.name: ep.load() for ep in pkg_resources.iter_entry_points('vsgen.projects')}
    assert 'demo' in project_classes, 'Entry Point "demo" not in "vsgen.projects" Entry Point collection'
    assert project_classes['demo'] == vsgendemo.projects.VSGAutoDemoProject, 'Entry Point "demo" does not resolve to "vsgendemo.projects.VSGEntryPointProject"'


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
        self._root = os.path.dirname(__main__.__file__)

        self._data = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'data'))
        self.assertTrue(os.path.isdir(self._data), 'Test data directory "{}" does not exist'.format(self._data))

        self._output = os.path.normpath(os.path.join(self._data, '_output'))
        self.assertFalse(os.path.exists(self._output), 'Test output directory {} already exits!'.format(self._output))

        self._file = os.path.normpath(os.path.join(self._data, 'vsgencfg', 'setup.cfg'))
        self.assertTrue(os.path.isfile(self._file), 'Test configuration file "{}" does not exist'.format(self._file))

    def tearDown(self):
        """
        The class specific tearDown method
        """
        if os.path.exists(self._output):
            shutil.rmtree(self._output)

    def test_configuration_file_success(self):
        """
        Tests the expected workflow.
        """
        result = __main__.main([__main__.__file__, 'generate', self._file])
        self.assertEqual(result, 0)


class TestIntegrationAuto(unittest.TestCase):
    """
    Tests the Solution and Project Generation from a directory.
    """

    def setUp(self):
        """
        The class specific setUp method
        """
        self._root = os.path.dirname(__main__.__file__)
        self._name = 'vsgen-auto'

        self._solution = os.path.normpath(os.path.join(self._root, self._name + '.sln'))
        self.assertFalse(os.path.exists(self._solution), 'Test output solution {} already exits!'.format(self._solution))

        self._project = os.path.normpath(os.path.join(self._root, self._name + '.pyproj'))
        self.assertFalse(os.path.exists(self._project), 'Test output project {} already exits!'.format(self._project))

    def tearDown(self):
        """
        The class specific tearDown method
        """
        # Remove the output directory
        if os.path.exists(self._solution):
            os.remove(self._solution)

        # Remove the output directory
        if os.path.exists(self._project):
            os.remove(self._project)

    def test_auto_uccess(self):
        """
        Tests the expected workflow.
        """
        result = __main__.main([__main__.__file__, 'auto', 'demo', '--root', self._root, '--name', self._name])
        self.assertEqual(result, 0)

if __name__ == '__main__':
    unittest.main()
