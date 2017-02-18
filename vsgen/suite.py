# -*- coding: utf-8 -*-
"""
This module provides all functionality for VSGen's suite functionality.

The module defines the class VSGSuite.  The VSGSuite class groups a collection of solutions and projects into a single class.
"""
import sys
import os
import inspect
import importlib
import argparse

from vsgen.solution import VSGSolution
from vsgen.writer import VSGWriteCommand
from vsgen.register import VSGRegisterCommand
from vsgen.util.config import VSGConfigParser


class VSGSuite(object):
    """
    The VSGSuite class groups a collection of solutions and projects into a single class.
    """
    def __init__(self, config):
        """
        Constructor.

        :param obj config: The instance of the VSGConfigParser class
        """
        # Resolve the root path
        root = config.get('vsgen', 'root', fallback=None)
        if not root:
            raise ValueError('Expected option "root" in section [vsgen].')
        if not os.path.isdir(root):
            raise ValueError('Expected option "root" (%s) does not resolve to valid directory.' % root)

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
        if filename not in config.read([filename]):
            raise ValueError('Could not read VSG configuration file %s.' % filename)

        # set the root
        root = config.get('vsgen', 'root')
        root = os.path.normpath(os.path.join(os.path.dirname(filename), root))
        config.set('vsgen', 'root', root)

        return VSGSuite(config)

    @classmethod
    def make_parser(cls, **kwargs):
        """
        Creates a :class:`~argparse.ArgumentParser` instances to work with VSGSuite classes.

        :param kwargs:  List of additional keyworded arguments to be passed into the :class:`~argparse.ArgumentParser`.
        :return:  A :class:`~argparse.ArgumentParser` instance.
        """
        # Build a parent parser
        parser = argparse.ArgumentParser(**kwargs)

        # Add multiple sub-commands:
        subparsers = parser.add_subparsers(help='Available commands.', dest='suite_commands')

        # 'Generate' command
        file_parser = subparsers.add_parser('generate', help='Generates solutions and projects based on one or more configuration files.')
        file_parser.add_argument('configuration_filenames', metavar='file', nargs='+', help='The configuration file that contains the [vsgen.*] sections contains the vsgen input.')

        # 'Auto' command
        auto_parser = subparsers.add_parser('auto', help='Automatically generates a solution and project collection from vsgen preset and a single directory.')

        # Build a subparser for each type of project
        suite_parsers = auto_parser.add_subparsers(help='Available Project Types.', dest='suite_type')
        for t in cls.suite_types():
            try:
                suite_class = cls.suite_class(t)
            except ValueError:
                continue
            suite_parser = suite_class.make_parser(add_help=False)
            suite_parsers.add_parser(t, help='Automatically generates a solution and {} project from a single directory.'.format(t), parents=[suite_parser])
        return parser

    @classmethod
    def from_args(cls, **kwargs):
        """
        Generates one or more VSGSuite instances from command line arguments.

        :param kwargs:  List of additional keyworded arguments to be passed into the VSGSuite defined in the :meth:`~VSGSuite.make_parser` method.
        """
        # Create a VSGSuite for each filename on the command line.
        if kwargs.get('suite_commands', None) == 'generate':
            filenames = getattr(kwargs, 'configuration_filenames', [])
            return [cls.from_file(filename) for f in filenames]

        # Create a VSGSuit from the target directory and override commands
        if kwargs.get('suite_commands', None) == 'auto':
            type = kwargs.get('suite_type', None)
            return [cls.from_directory('', type, **kwargs)]

        # Create nothing.
        return []

    @classmethod
    def suite_types(cls):
        """
        Retreieve the list of possible suite types available.

        :return: A list of suite type names.
        """
        data = os.path.join(os.path.dirname(sys.modules['vsgen'].__file__), 'data')
        return [os.path.splitext(os.path.basename(f))[0] for f in os.listdir(data)]

    @classmethod
    def suite_class(cls, type):
        """
        Creates an VSGSuite instance from a filename.

        :param str filename:  The fully qualified path to the VSG configuration file.
        :param str type:  The configuration type to generate.
        """
        try:
            module = importlib.import_module("vsgen.{}".format(type))
        except ImportError:
            raise ValueError('Cannot resolve type "{}" to a recognised vsgen suite type.'.format("type"))
        suite_classes = [obj for name, obj in inspect.getmembers(module) if getattr(obj, '__type__', None) == type]
        if len(suite_classes) == 0:
            raise ValueError('Cannot resolve a recognised suite type for type [{}].'.format(type))
        if len(suite_classes) > 1:
            raise ValueError('Too many suite classes resolved to ambiguous type [{}].'.format(type))

        return suite_classes[0]

    @classmethod
    def from_directory(cls, directory, type, **kwargs):
        """
        Creates an VSGSuite instance from a filename.

        :param str filename:  The fully qualified path to the VSG configuration file.
        :param str type:  The configuration type to generate.
        :param kwargs:  List of additional keyworded arguments to be passed into the VSGSuite.
        """
        # Resolve the suite class from the type
        suite_class = cls.suite_class(type)

        # Merge the default and any additional, maybe override, params.
        params = {
            'root': os.path.abspath(directory),
            'name': os.path.basename(os.path.abspath(directory))
        }
        params.update(kwargs)
        return suite_class(**params)

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
