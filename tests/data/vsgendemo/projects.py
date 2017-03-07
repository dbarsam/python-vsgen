# -*- coding: utf-8 -*-
"""
This module provides the neccessary project defintions for VSGDemo's PTVS projects
"""
import os
import uuid
import errno

from vsgen import VSGProject
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


class VSGDemoBaseProject(VSGProject):
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
        Creates the PTVS project file.
        """
        npath = os.path.normpath(self.FileName)
        (filepath, filename) = os.path.split(npath)
        try:
            os.makedirs(filepath)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

        projectFileName = os.path.normpath(self.FileName)
        projectRelativeHome = os.path.relpath(self.ProjectHome, filepath)
        projectRelativeSearchPath = [os.path.relpath(path, self.ProjectHome) for path in self.SearchPath] if self.SearchPath else [self.ProjectHome]
        projectRelativeWorkingDirectory = os.path.relpath(self.WorkingDirectory, self.ProjectHome)
        projectRelativeOutputPath = os.path.relpath(self.OutputPath, self.ProjectHome)
        projectRelativeStartupFile = os.path.relpath(self.StartupFile, self.ProjectHome) if self.StartupFile else None
        with open(projectFileName, 'wt') as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n')
            f.write('<Project ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003" DefaultTargets="Build">\n')
            f.write('  <PropertyGroup>\n')
            f.write('    <Configuration Condition=" \'$(Configuration)\' == \'\' ">Debug</Configuration>\n')
            f.write('    <SchemaVersion>2.0</SchemaVersion>\n')
            f.write('    <ProjectGuid>{{{0}}}</ProjectGuid>\n'.format(self.lower(self.GUID)))
            f.write('    <ProjectHome>{0}</ProjectHome>\n'.format(projectRelativeHome))
            f.write('    <StartupFile>{0}</StartupFile>\n'.format(projectRelativeStartupFile))
            f.write('    <SearchPath>{0}</SearchPath>\n'.format(';'.join(projectRelativeSearchPath)))
            f.write('    <WorkingDirectory>{0}</WorkingDirectory>\n'.format(projectRelativeWorkingDirectory))
            f.write('    <OutputPath>{0}</OutputPath>\n'.format(projectRelativeOutputPath))
            f.write('    <RootNamespace>{0}</RootNamespace>\n'.format(self.RootNamespace))
            f.write('    <IsWindowsApplication>{0}</IsWindowsApplication>\n'.format(self.IsWindowsApplication))
            f.write('    <LaunchProvider>Standard Python launcher</LaunchProvider>\n')
            f.write('    <CommandLineArguments />\n')
            f.write('    <InterpreterPath />\n')
            f.write('    <InterpreterArguments>{0}</InterpreterArguments>\n'.format(" ".join(self.PythonInterpreterArgs)))
            f.write('    <VisualStudioVersion Condition="\'$(VisualStudioVersion)\' == \'\'">10.0</VisualStudioVersion>\n')
            f.write('    <VSToolsPath Condition="\'$(VSToolsPath)\' == \'\'">$(MSBuildExtensionsPath32)\Microsoft\VisualStudio\\v$(VisualStudioVersion)</VSToolsPath>\n')
            f.write('  </PropertyGroup>\n')
            f.write('  <PropertyGroup Condition=" \'$(Configuration)\' == \'Debug\' ">\n')
            f.write('    <DebugSymbols>true</DebugSymbols>\n')
            f.write('    <EnableUnmanagedDebugging>false</EnableUnmanagedDebugging>\n')
            f.write('  </PropertyGroup>\n')
            f.write('  <PropertyGroup Condition=" \'$(Configuration)\' == \'Release\' ">\n')
            f.write('    <DebugSymbols>true</DebugSymbols>\n')
            f.write('    <EnableUnmanagedDebugging>false</EnableUnmanagedDebugging>\n')
            f.write('  </PropertyGroup>\n')
            f.write('  <PropertyGroup>\n')
            f.write('    <VisualStudioVersion Condition=" \'$(VisualStudioVersion)\' == \'\' ">10.0</VisualStudioVersion>\n')
            f.write('    <PtvsTargetsFile>$(MSBuildExtensionsPath32)\Microsoft\VisualStudio\\v$(VisualStudioVersion)\Python Tools\Microsoft.PythonTools.targets</PtvsTargetsFile>\n')
            f.write('  </PropertyGroup>\n')

            if self.ContentFiles:
                f.write('  <ItemGroup>\n')
                for fn in [os.path.relpath(path, self.ProjectHome) for path in sorted(self.ContentFiles, key=self.lower)]:
                    f.write('    <Content Include="' + fn + '" />\n')
                f.write('  </ItemGroup>\n')

            if self.CompileFiles:
                f.write('  <ItemGroup>\n')
                for fn in [os.path.relpath(path, self.ProjectHome) for path in sorted(self.CompileFiles, key=self.lower)]:
                    f.write('    <Compile Include="' + fn + '" />\n')
                f.write('  </ItemGroup>\n')

            if self.Directories or self.ContentFiles or self.CompileFiles:
                fileDirectories = [os.path.dirname(filename) for filename in self.CompileFiles + self.ContentFiles]
                relativeDirectories = [os.path.relpath(path, self.ProjectHome) for path in self.Directories + fileDirectories]
                directories = set(relativeDirectories)

                # We need separate entries for parent directories of directories in the list
                for path in relativeDirectories:
                    subpath = os.path.dirname(path)
                    while subpath:
                        directories.add(subpath)
                        subpath = os.path.dirname(subpath)

                f.write('  <ItemGroup>\n')
                for fn in sorted(directories):
                    f.write('    <Folder Include="' + fn + '" />\n')
                f.write('  </ItemGroup>\n')

            if self.PythonInterpreters:
                f.write('  <ItemGroup>\n')
                for interpreter in self.PythonInterpreters:
                    f.write('    <InterpreterReference Include="{{{0}}}\\{1}" />\n'.format(self.upper(interpreter.BaseInterpreter), interpreter.Version))
                f.write('  </ItemGroup>\n')

            f.write('  <Import Project="$(PtvsTargetsFile)" Condition="Exists($(PtvsTargetsFile))" />\n')
            f.write('  <Import Project="$(MSBuildToolsPath)\Microsoft.Common.targets" Condition="!Exists($(PtvsTargetsFile))" />\n')
            f.write('</Project>')

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
