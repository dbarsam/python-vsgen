# -*- coding: utf-8 -*-
"""
This module provides the neccessary defintions to generate a Project File.
"""

import os
import csv
import fnmatch
import uuid
import errno

from vsgen.project import VSGProject
from vsgen.ptvs.interpreter import PTVSInterpreter


class PTVSProject(VSGProject):
    """
    PTVSProject extends :class:`~vsgen.project.VSGProject` with data and logic needed to create a `.pyproj` file.

    :ivar list  SearchPath:             The list of absolute directories that will be added to the Python search path; if not provide the value is [].
    :ivar bool  IsWindowsApplication:   The boolean flag to launch the application as a `.pyw` file or not; if not provide the value is False.
    :ivar list  PythonInterpreter:      The active interpreter. Either None or one of the values specified in PythonInterpreters or VirtualEnvironments; if not provide the value is None.
    :ivar list  PythonInterpreterArgs:  The active interpreter's arguments.  If not provide the value is [].
    :ivar list  PythonInterpreters:     The list of pyInterpreters that are base interpreters that will be available; if not provide the value is [].
    :ivar list  VirtualEnvironments:    The list of pyInterpreters that are virtual environments that will be available; if not provide the value is [].
    """
    __project_type__ = 'ptvs'

    __writable_name__ = "Visual Studio PTVS Project"

    __registerable_name__ = "Visual Studio PTVS Python Interpreter"

    def __init__(self, **kwargs):
        """
        Constructor.

        :param kwargs:         List of arbitrary keyworded arguments to be processed as instance variable data
        """
        super(PTVSProject, self).__init__(**kwargs)

    def _import(self, datadict):
        """
        Internal method to import instance variables data from a dictionary

        :param dict datadict: The dictionary containing variables values.
        """
        super(PTVSProject, self)._import(datadict)
        self.SearchPath = datadict.get("SearchPath", [])
        self.IsWindowsApplication = datadict.get("IsWindowsApplication", False)
        self.PythonInterpreter = datadict.get("PythonInterpreter", None)
        self.PythonInterpreterArgs = datadict.get("PythonInterpreterArgs", [])
        self.PythonInterpreters = datadict.get("PythonInterpreters", [])
        self.VirtualEnvironments = datadict.get("VirtualEnvironments", [])

    @classmethod
    def from_section(cls, config, section, **kwargs):
        """
        Creates a :class:`~vsgen.ptvs.interpreter.PTVSProject` from a :class:`~configparser.ConfigParser` section.

        :param ConfigParser config:   A :class:`~configparser.ConfigParser` instance.
        :param str          section:  A :class:`~configparser.ConfigParser` section key.
        :param              kwargs:   List of additional keyworded arguments to be passed into the :class:`~vsgen.ptvs.project.PTVSProject`.
        :return:                      A valid :class:`~vsgen.ptvs.project.PTVSProject` instance if succesful; None otherwise.
        """
        p = super(PTVSProject, cls).from_section(config, section, **kwargs)

        p.SearchPath = config.getdirs(section, 'search_path', fallback=p.SearchPath)
        p.IsWindowsApplication = config.getboolean(section, 'is_windows_application', fallback=p.IsWindowsApplication)
        p.PythonInterpreterArgs = config.getlist(section, 'python_interpreter_args', fallback=p.PythonInterpreterArgs)

        interpreter = config.get(section, 'python_interpreter', fallback=None)
        interpreters = {n: [i for i in PTVSInterpreter.from_section(config, n, VSVersion=p.VSVersion)] for n in config.getlist(section, 'python_interpreters')}
        p.PythonInterpreters = [i for v in interpreters.values() for i in v]
        p.PythonInterpreter = next((i for i in interpreters.get(interpreter, [])), None)

        virtual_environments = config.getlist(section, 'python_virtual_environments', fallback=[])
        p.VirtualEnvironments = [ve for n in virtual_environments for ve in PTVSInterpreter.from_section(config, n, VSVersion=p.VSVersion)]

        return p

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
        projectInterpreter = self.PythonInterpreter or next((p for p in self.PythonInterpreters), None)
        with open(projectFileName, 'wt') as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n')
            f.write('<Project ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003" DefaultTargets="Build">\n')
            f.write('  <PropertyGroup>\n')
            f.write('    <Configuration Condition=" \'$(Configuration)\' == \'\' ">Debug</Configuration>\n')
            f.write('    <SchemaVersion>2.0</SchemaVersion>\n')
            f.write('    <ProjectGuid>{{{0}}}</ProjectGuid>\n'.format(self.lower(self.GUID)))
            f.write('    <ProjectHome>{0}</ProjectHome>\n'.format(projectRelativeHome))
            if projectRelativeStartupFile:
                f.write('    <StartupFile>{0}</StartupFile>\n'.format(projectRelativeStartupFile))
            else:
                f.write('    <StartupFile />\n')
            f.write('    <SearchPath>{0}</SearchPath>\n'.format(';'.join(projectRelativeSearchPath)))
            f.write('    <WorkingDirectory>{0}</WorkingDirectory>\n'.format(projectRelativeWorkingDirectory))
            f.write('    <OutputPath>{0}</OutputPath>\n'.format(projectRelativeOutputPath))
            f.write('    <RootNamespace>{0}</RootNamespace>\n'.format(self.RootNamespace))
            f.write('    <IsWindowsApplication>{0}</IsWindowsApplication>\n'.format(self.IsWindowsApplication))
            if projectInterpreter:
                f.write('    <InterpreterId>{{{0}}}</InterpreterId>\n'.format(self.lower(projectInterpreter.GUID)))
                f.write('    <InterpreterVersion>{0}</InterpreterVersion>\n'.format(projectInterpreter.Version))
            f.write('    <LaunchProvider>Standard Python launcher</LaunchProvider>\n')
            f.write('    <CommandLineArguments />\n')
            f.write('    <InterpreterPath />\n')
            if self.PythonInterpreterArgs:
                f.write('    <InterpreterArguments>{0}</InterpreterArguments>\n'.format(" ".join(self.PythonInterpreterArgs)))
            else:
                f.write('    <InterpreterArguments />\n')
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

            if self.VirtualEnvironments:
                f.write('  <ItemGroup>\n')
                for venv in self.VirtualEnvironments:
                    f.write('    <Interpreter Include="{0}">\n'.format(os.path.relpath(venv.Path, self.ProjectHome)))
                    f.write('      <Id>{{{0}}}</Id>\n'.format(self.upper(venv.GUID)))
                    f.write('      <BaseInterpreter>{{{0}}}</BaseInterpreter>\n'.format(self.upper(venv.BaseInterpreter)))
                    f.write('      <Version>{0}</Version>\n'.format(venv.Version))
                    f.write('      <Description>{0}</Description>\n'.format(venv.Description))
                    f.write('      <InterpreterPath>{0}</InterpreterPath>\n'.format(venv.InterpreterPath))
                    f.write('      <WindowsInterpreterPath>{0}</WindowsInterpreterPath>\n'.format(venv.WindowsInterpreterPath))
                    f.write('      <LibraryPath>{0}</LibraryPath>\n'.format(venv.LibraryPath))
                    f.write('      <PathEnvironmentVariable>{0}</PathEnvironmentVariable>\n'.format(venv.PathEnvironmentVariable))
                    f.write('      <Architecture>{0}</Architecture>\n'.format(venv.Architecture))
                    f.write('    </Interpreter>\n')
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
