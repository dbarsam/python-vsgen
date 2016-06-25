# -*- coding: utf-8 -*-
"""
This module provides all functionality for extending Python's suite class of functionality.

The module defines the class VSGSuite.  The VSGSuite class groups the different functionalities into a single class.
"""
import sys
import os
import inspect
import importlib

from vsgen.solution import VSGSolution
from vsgen.writer import VSGWriteCommand
from vsgen.register import VSGRegisterCommand
from vsgen.util.config import VSGConfigParser


class VSGSuite(object):

    def __init__(self, config):
        """
        Constructor.

        :param obj config: The instance of the VSGConfigParser class
        """
        # Resolve the root path
        root = config.get('vsgen', 'root', fallback=None)
        if not root:
            raise ValueError('Expected option "root" in section [vsgen].')

        # Build the VSG Solutions
        self._solutions = [self._getsolution(config, s) for s in config.sections() if 'vsgen.solution' in s]

        return super(VSGSuite, self).__init__()

    def _getsolution(self, config, section, **kwargs):
        """
        Creates a VSG solution from a configparser instance.

        :param obj config: The instance of the configparser class
        :param str section: The section name to read.
        :param kwargs:  List of additional keyworded arguments to be passed into the VSGSolution.
        :return: A valid VSGSolution instance if succesful; None otherwise.
        """
        if section not in config:
            raise ValueError('Section [{}] not found in [{}]'.format(section, ', '.join(config.sections())))

        s = VSGSolution(**kwargs)

        s.Name = config.get(section, 'name', fallback=s.Name)
        s.FileName = os.path.normpath(config.get(section, 'filename', fallback=s.FileName))
        s.VSVersion = config.getfloat(section, 'visual_studio_version', fallback=s.VSVersion)
        if not s.VSVersion:
            raise ValueError('Solution section [%s] requires a value for Visual Studio Version (visual_studio_version)' % section)

        project_sections = config.getlist(section, 'projects', fallback=[])
        for project_section in project_sections:
            project = self._getproject(config, project_section, VSVersion=s.VSVersion)
            s.Projects.append(project)

        return s

    def _getproject(self, config, section, **kwargs):
        """
        Creates a VSG project from a configparser instance.

        :param obj config: The instance of the configparser class
        :param str section: The section name to read.
        :param kwargs:  List of additional keyworded arguments to be passed into the VSGProject.
        :return: A valid VSGProject instance if succesful; None otherwise.
        """
        if section not in config:
            raise ValueError('Section [{}] not found in [{}]'.format(section, ', '.join(config.sections())))

        type = config.get(section, 'type', fallback=None)
        if not type:
            raise ValueError('Section [{}] mandatory option "{}" not found'.format(section, "type"))

        try:
            module = importlib.import_module("vsgen.{}".format(type))
        except ImportError:
            raise ValueError('Cannot resolve option "{}" to a recognised type in section [{}].'.format("type", section))

        project_classes = [obj for name, obj in inspect.getmembers(module) if getattr(obj, '__project_type__', None) == type]
        if len(project_classes) == 0:
            raise ValueError('Cannot resolve option "{}" ("{}") to a recognised project type in section [{}].'.format("type", type, section))
        if len(project_classes) > 1:
            raise ValueError('Too many projects resolved to ambiguous option "{}" ("{}") in section [{}].'.format("type", type, section))

        p = project_classes[0].from_section(config, section, **kwargs)
        return p

    @classmethod
    def from_file(cls, filename):
        """
        Creates an VSGSuite instance from a filename.

        :param str filename:  The fully qualified path to the VSG configuration file.
        """
        # Read the configuration file
        config = VSGConfigParser()
        if filename not in config.read(filename):
            raise ValueError('Could not read VSG configuration file %s.' % filename)

        # set the root
        root = config.get('vsgen', 'root')
        root = os.path.normpath(os.path.join(os.path.dirname(filename), root))
        config.set('vsgen', 'root', root)

        return VSGSuite(config)

    @classmethod
    def from_directory(cls, directory, type):
        """
        Creates an VSGSuite instance from a filename.

        :param str filename:  The fully qualified path to the VSG configuration file.
        :param str filename:  The configuration type to generate.
        """
        filename = os.path.join(os.path.dirname(sys.modules['vsgen'].__file__), 'data', '{}.cfg'.format(type))

        # Read the configuration file
        config = VSGConfigParser()
        if filename not in config.read(filename):
            raise ValueError('Could not read VSG configuration file %s.' % filename)

        # set the root
        config.set('vsgen', 'root', os.path.normpath(directory))
        config.set('vsgen', 'name', os.path.basename(directory))

        return VSGSuite(config)

    def write(self, parallel=True):
        """
        Writes the configuration to disk.
        """
        # Write the Solution files
        solutions = sorted(self._solutions, key=lambda x: x.Name)
        with VSGWriteCommand('Writing VSG Solution', solutions, parallel) as command:
            command.execute()

        # Write the Projects files
        projects = set(sorted((p for s in solutions for p in s.Projects), key=lambda x: x.Name))
        with VSGWriteCommand('Writing VSG Projects', projects, parallel) as command:
            command.execute()

        # Register the registerables
        registerables = set(sorted((p for s in solutions for p in s.Projects), key=lambda x: x.Name))
        with VSGRegisterCommand('Registering Project Registerables', registerables) as command:
            command.execute()
