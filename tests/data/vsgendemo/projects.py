# -*- coding: utf-8 -*-
"""
This module provides the neccessary project defintions for VSGDemo's PTVS projects
"""
import os
import uuid
import errno

from vsgen import VSGProject
from vsgen.writer import VSGJinjaRenderer
from vsgen.writer import VSGWritable, VSGJinjaRenderer
from vsgen.register import VSGRegisterable, VSGRegisterCommand
from vsgendemo.settings import VSGDemoSettings


class VSGDemoMockInterpreter(VSGRegisterable):
    pass


class VSGDemoMockRegisterable(VSGRegisterable):
    """
    PTVSInterpreter encapsulates the logic and data used to describe a Python interpreter or virtual environments

    :ivar uuid BaseInterpreter:         The GUID of the base Python Interpreter.
    :ivar str  Version:                 The major.minor version string; if not provide the value is "".
    """
    __registerable_name__ = "VSDemo Mock Registerable"

    def __init__(self, **kwargs):
        """
        Constructor.

        :param kwargs:         List of arbitrary keyworded arguments to be processed as instance variable data
        """
        super(VSGDemoMockRegisterable, self).__init__()
        self.BaseInterpreter = uuid.uuid1()
        self.Version = "2.7"

    def register(self):
        """
        Registers the environment into the windows registry.

        :note: We're explictly writing the environment to the registry to facilitate sharing. See `How to share pyproj across team with custom environments <https://pytools.codeplex.com/workitem/2765>`_ for motivation.
        """
        pass


class VSGDemoBaseProject(VSGProject, VSGDemoSettings, VSGRegisterable, VSGJinjaRenderer):
    """
    VSGDemoBaseProject extends :class:`~vsgen.project.VSGProject` with data and logic needed to create a demo project that is really a simplified `.pyproj` file.

    :ivar list  SearchPath:             The list of absolute directories that will be added to the Python search path; if not provide the value is [].
    :ivar bool  IsWindowsApplication:   The boolean flag to launch the application as a `.pyw` file or not; if not provide the value is False.
    :ivar list  PythonInterpreter:      The active interpreter. Either None or one of the values specified in PythonInterpreters or VirtualEnvironments; if not provide the value is None.
    :ivar list  PythonInterpreterArgs:  The active interpreter's arguments.  If not provide the value is [].
    :ivar list  PythonInterpreters:     The list of pyInterpreters that are base interpreters that will be available; if not provide the value is [].
    """
    __project_type__ = 'demo'

    __writable_name__ = "VSGen Simple Demo Project"

    __registerable_name__ = "Visual Studio Demo Registerable Type"

    __jinja_template__ = os.path.abspath(os.path.join(os.path.dirname(__file__), 'vsgendemoproject.jinja'))

    def __init__(self, name, rootpath, **kwargs):
        """
        Constructor.

        :param kwargs:         List of arbitrary keyworded arguments to be processed as instance variable data
        """
        super(VSGDemoBaseProject, self).__init__(**kwargs)
        self.Name = name
        self.FileName = os.path.join(VSGDemoSettings.ProjectRoot, '{0}.pyproj'.format(name.lower()))
        self.ProjectHome = rootpath
        self.SearchPath = [rootpath]
        self.WorkingDirectory = rootpath
        self.OutputPath = rootpath
        self.RootNamespace = 'VSGDemo'
        self.PythonInterpreters = [VSGDemoMockRegisterable()]
        self.PythonInterpreterArgs = ['-B']
        self.IsWindowsApplication = True
        self.CompileInFilter = ['*.py', '*.pyw']
        self.ContentInFilter = ['*.bat', '*.txt', '*.cmd', '*.ico', '*.png', '*.md']

    def initialize(self):
        """
        Initializes the VSGSolution by overriding the default values with instance specific values.
        """
        pass

    def write(self):
        """
        Creates a simple PTVS project file.
        """
        filters = {
            'MSGUID': lambda x: ('{%s}' % x).upper(),
            'relprojhome': lambda x: os.path.relpath(x, self.ProjectHome),
            'relprojfile': lambda x: os.path.relpath(x, self.FileName)
        }

        context = {
            'pyproj': self,
        }
        return self.render(self.__jinja_template__, self.FileName, context, filters)

    def register(self):
        """
        Registers the project's python environments.
        """
        # Interpretters
        for i in set(self.PythonInterpreters):
            i.register()


class VSGCoreProject(VSGDemoBaseProject):
    """
    VSGDemoProject provides a :class:`~vsgen.project.VSGProject` for the main VSG python package.
    """
    RootPath = os.path.join(VSGDemoSettings.MainRoot, 'vsgen')

    def __init__(self, **kwargs):
        super(VSGCoreProject, self).__init__('VSG', self.RootPath, **kwargs)
        self.insert_files(self.RootPath)


class VSGDemoProject(VSGDemoBaseProject):
    """
    VSGDemoProject provides a :class:`~vsgen.project.VSGProject` for the VSGDemo python package.
    """
    RootPath = os.path.join(VSGDemoSettings.MainRoot, 'tests', 'data', 'vsgendemo')

    def __init__(self, **kwargs):
        super(VSGDemoProject, self).__init__('VSGDemo', self.RootPath, **kwargs)
        self.insert_files(self.RootPath)


class VSGAutoDemoProject(VSGDemoBaseProject):
    """
    VSGAutoDemoProject provides a :class:`~vsgen.project.VSGProject` class for vsgendemo's entry point plugin data.
    """

    def __init__(self, **kwargs):
        super(VSGAutoDemoProject, self).__init__('VSG', '', **kwargs)
