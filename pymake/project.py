# -*- coding: utf-8 -*-
"""
This module provides the neccessary defintions to generate a Project File.
"""

import os
import csv
import fnmatch
import uuid

from pymake.writer import PyWritable

class PymakeProject(PyWritable):
    """
    PymakeProject encapsulates the data and logic needed to create a *.pyproject file.

    :ivar GUID:                   The GUID of the project; if not provided one is generated automatically.
    :ivar FileName:               The absolute filename of the project file; if not provided the value is ""
    :ivar Name:                   The display name of the project; if not provide the value is "".
    :ivar SearchPath:             The list of absolute directories that will be added to the Python search path; if not provide the value is [].
    :ivar WorkingDirectory:       The absolute directory that will be the working directory of the project; if not provide the value is ""
    :ivar OutputPath:             The absolute directory that will be the output directory of the project; if not provide the value is "".
    :ivar RootNamespace:          The name of the root namespace of the project; if not provide the value is "". <ignored >
    :ivar ProjectHome:            The absolute directory of the project's source root folder; if not provide the value is ""
    :ivar StartupFile:            The absolute path to the Startup file; if not provide the value is ""
    :ivar CompileFiles:           The list of absolute files that will comprise the projects compile group; if not provide the value is [].
    :ivar ContentFiles:           The list of absolute files that will comprise the projects content group; if not provide the value is [].
    :ivar Directories:            The list of absolute directories that will comprise the projects directory group; if not provide the value is [].
    :ivar IsWindowsApplication:   The boolean flag to launch the application as a *.pyw file or not; if not provide the value is False.
    :ivar DirectoryInFilter:      A list of strings matching exactly with directories to be explicitly included during the item generation step; if not provided the value is [].
    :ivar DirectoryExFilter:      A list of strings matching exactly with directories to be explicitly excluded during the item generation step; if not provided the value is [].
    :ivar CompileInFilter:        A list of strings matching exactly with file extensions ('.ext') of compile files to be included during the item generation step; if not provide the value is [].
    :ivar ContentInFilter:        A list of strings matching exactly with file extensions ('.ext') of content files to be included during the item generation step; if not provide the value is [].
    :ivar PythonInterpreter:      The active interpreter. Either None or one of the values specified in PythonInterpreters or VirtualEnvironments; if not provide the value is None.
    :ivar PythonInterpreterArgs:  The active interpreter's arguments.  If not provide the value is [].
    :ivar PythonInterpreters:     The list of pyInterpreters that are base interpreters that will be available; if not provide the value is [].
    :ivar VirtualEnvironments:    The list of pyInterpreters that are virtual environments that will be available; if not provide the value is [].
    """
    __writable_name__ = "Pymake Project"

    def __init__(self, **kwargs):
        """
        Constructor.

        :param **kwargs:         List of arbitrary keyworded arguments to be processed as instance variable data
        """
        super(PymakeProject, self).__init__()
        self._import(kwargs)

    def _import(self, datadict):
        """
        Internal method to import instance variables data from a dictionary

        :param datadict: The dictionary containing variables values.
        """
        self.GUID                  = datadict.get("GUID", uuid.uuid1())
        self.FileName              = datadict.get("FileName","")
        self.Name                  = datadict.get("Name","")
        self.SearchPath            = datadict.get("SearchPath",[])
        self.WorkingDirectory      = datadict.get("WorkingDirectory","")
        self.OutputPath            = datadict.get("OutputPath","")
        self.RootNamespace         = datadict.get("RootNamespace","")
        self.ProjectHome           = datadict.get("ProjectHome","" )
        self.StartupFile           = datadict.get("StartupFile","" )
        self.CompileFiles          = datadict.get("CompileFiles",[] )
        self.ContentFiles          = datadict.get("ContentFiles",[])
        self.Directories           = datadict.get("Directories",[])
        self.IsWindowsApplication  = datadict.get("IsWindowsApplication",False)
        self.DirectoryInFilter     = datadict.get("DirectoryInFilter",[])
        self.DirectoryExFilter     = datadict.get("DirectoryExFilter",[])
        self.CompileInFilter       = datadict.get("CompileInFilter",[])
        self.CompileExFilter       = datadict.get("CompileExFilter",[])
        self.ContentInFilter       = datadict.get("ContentInFilter",[])
        self.ContentExFilter       = datadict.get("ContentExFilter",[])
        self.PythonInterpreter     = datadict.get("PythonInterpreter",None)
        self.PythonInterpreterArgs = datadict.get("PythonInterpreterArgs",[])
        self.PythonInterpreters    = datadict.get("PythonInterpreters",[])
        self.VirtualEnvironments   = datadict.get("VirtualEnvironments",[])

    def insert_files(self, rootpath, directoryInFilter=None, directoryExFilter=None, compileInFilter=None, compileExFilter=None, contentInFilter=None, contentExFilter=None):
        """
        Inserts files by recursive traversing the rootpath and inserting files according the addition filter parameters.
        
        :param rootpath:           The absolute path to the root directory.
        :param directoryInFilter:  A list of strings matching exactly with directories to be included.  A None value will default to self.DirectoryInFilter.
        :param directoryExFilter:  A list of strings matching exactly with directories to be excluded.  A None value will default to self.DirectoryExFilter.
        :param compileInFilter:    A list of strings matching exactly with file extensions ('.ext') of compile files to be included.  A None value will default to self.CompileInFilter. 
        :param compileExFilter:    A list of strings matching exactly with file extensions ('.ext') of compile files to be included.  A None value will default to self.CompileExFilter. 
        :param contentInFilter:    A list of strings matching exactly with file extensions ('.ext') of content files to be includes.  A None value will default to self.ContentInFilter.        
        :param contentExFilter:    A list of strings matching exactly with file extensions ('.ext') of content files to be includes.  A None value will default to self.ContentExFilter.
        """
        # Overrides
        directoryInFilter = self.DirectoryInFilter if directoryInFilter == None else directoryInFilter
        directoryExFilter = self.DirectoryExFilter if directoryExFilter == None else directoryExFilter
        compileInFilter   = self.CompileInFilter if compileInFilter == None else compileInFilter
        compileExFilter   = self.CompileExFilter if compileExFilter == None else compileExFilter
        contentInFilter   = self.ContentInFilter if contentInFilter == None else contentInFilter
        contentExFilter   = self.ContentExFilter if contentExFilter == None else contentExFilter

        # Directory Path Clean-up
        if directoryInFilter:
            directoryInFilter = [os.path.normcase(os.path.normpath(d)) for d in directoryInFilter]
        if directoryExFilter:
            directoryExFilter = [os.path.normcase(os.path.normpath(d)) for d in directoryExFilter]

        matches = []
        for root, dirnames, filenames in os.walk(rootpath):

            searchdir = os.path.normpath(os.path.normcase(root))
            
            # Manually exclude
            if directoryExFilter and any(rootdir in searchdir for rootdir in directoryExFilter):
                dirnames[:] = []
            # If we have the Target or a Child of a target directory, add the files 
            elif not directoryInFilter or any(rootdir in searchdir for rootdir in directoryInFilter):
                for f in filenames:
                    ext = os.path.splitext(f)[1];
                    if compileExFilter and ext in compileExFilter:
                        continue
                    if not compileInFilter or ext in compileInFilter:
                        self.CompileFiles.append(os.path.join(root, f))
                    if contentExFilter and ext in contentExFilter:
                        continue
                    if not contentInFilter or ext in contentInFilter:
                        self.ContentFiles.append(os.path.join(root, f))
            # If we're not a root folder of a target we are in the wrong branch
            elif not any(searchdir in rootdir for rootdir in directoryInFilter):
                dirnames[:] = []

    def write(self):
        """
        Creates the PymakeProject
        """
        npath = os.path.normpath(self.FileName)
        (filepath, filename) = os.path.split(npath)
        if not os.path.exists(filepath):
            os.makedirs(filepath)

        projectFileName = os.path.normpath(self.FileName)
        projectRelativeHome = os.path.relpath(self.ProjectHome, filepath)
        projectRelativeSearchPath = [os.path.relpath(path, self.ProjectHome) for path in self.SearchPath] if self.SearchPath else [self.ProjectHome]
        projectRelativeWorkingDirectory = os.path.relpath(self.WorkingDirectory, self.ProjectHome);
        projectRelativeOutputPath = os.path.relpath(self.OutputPath, self.ProjectHome);
        projectRelativeStartupFile = os.path.relpath(self.StartupFile, self.ProjectHome) if self.StartupFile else None
        projectInterpreter = self.PythonInterpreter or next((p for p in self.PythonInterpreters), None)
        with open(projectFileName, 'wt') as f:
            f.write( '<?xml version="1.0" encoding="utf-8"?>\n' )
            f.write( '<Project ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003" DefaultTargets="Build">\n' )
            f.write( '  <PropertyGroup>\n' )
            f.write( '    <Configuration Condition=" \'$(Configuration)\' == \'\' ">Debug</Configuration>\n' )
            f.write( '    <SchemaVersion>2.0</SchemaVersion>\n' )
            f.write( '    <ProjectGuid>{{{0}}}</ProjectGuid>\n'.format(str(self.GUID).lower()) )
            f.write( '    <ProjectHome>{0}</ProjectHome>\n'.format(projectRelativeHome) )
            if projectRelativeStartupFile:
                f.write( '    <StartupFile>{0}</StartupFile>\n'.format(projectRelativeStartupFile) )
            else:
                f.write( '    <StartupFile />\n' )
            f.write( '    <SearchPath>{0}</SearchPath>\n'.format(';'.join(projectRelativeSearchPath)) )
            f.write( '    <WorkingDirectory>{0}</WorkingDirectory>\n'.format(projectRelativeWorkingDirectory) )
            f.write( '    <OutputPath>{0}</OutputPath>\n'.format(projectRelativeOutputPath) )
            f.write( '    <RootNamespace>{0}</RootNamespace>\n'.format(self.RootNamespace) )
            f.write( '    <IsWindowsApplication>{0}</IsWindowsApplication>\n'.format(self.IsWindowsApplication) )            
            if projectInterpreter:
                f.write( '    <InterpreterId>{{{0}}}</InterpreterId>\n'.format(str(projectInterpreter.GUID).lower()) )
                f.write( '    <InterpreterVersion>{0}</InterpreterVersion>\n'.format(projectInterpreter.Version) )
            f.write( '    <LaunchProvider>Standard Python launcher</LaunchProvider>\n' )
            f.write( '    <CommandLineArguments />\n' )
            f.write( '    <InterpreterPath />\n' )
            if self.PythonInterpreterArgs:
                f.write( '    <InterpreterArguments>{0}</InterpreterArguments>\n'.format(" ".join(self.PythonInterpreterArgs)))
            else:
                f.write( '    <InterpreterArguments />\n' )
            f.write( '    <VisualStudioVersion Condition="\'$(VisualStudioVersion)\' == \'\'">10.0</VisualStudioVersion>\n' )
            f.write( '    <VSToolsPath Condition="\'$(VSToolsPath)\' == \'\'">$(MSBuildExtensionsPath32)\Microsoft\VisualStudio\\v$(VisualStudioVersion)</VSToolsPath>\n' )
            f.write( '  </PropertyGroup>\n' )
            f.write( '  <PropertyGroup Condition=" \'$(Configuration)\' == \'Debug\' ">\n' )
            f.write( '    <DebugSymbols>true</DebugSymbols>\n' )
            f.write( '    <EnableUnmanagedDebugging>false</EnableUnmanagedDebugging>\n' )
            f.write( '  </PropertyGroup>\n' )
            f.write( '  <PropertyGroup Condition=" \'$(Configuration)\' == \'Release\' ">\n' )
            f.write( '    <DebugSymbols>true</DebugSymbols>\n' )
            f.write( '    <EnableUnmanagedDebugging>false</EnableUnmanagedDebugging>\n' )
            f.write( '  </PropertyGroup>\n' )
            f.write( '  <PropertyGroup>\n' )
            f.write( '    <VisualStudioVersion Condition=" \'$(VisualStudioVersion)\' == \'\' ">10.0</VisualStudioVersion>\n')
            f.write( '    <PtvsTargetsFile>$(MSBuildExtensionsPath32)\Microsoft\VisualStudio\\v$(VisualStudioVersion)\Python Tools\Microsoft.PythonTools.targets</PtvsTargetsFile>\n')
            f.write( '  </PropertyGroup>\n' )
  
            if self.ContentFiles:
                f.write( '  <ItemGroup>\n' )
                for fn in [os.path.relpath(path, self.ProjectHome) for path in sorted(self.ContentFiles,key=str.lower) ]:
                    f.write( '    <Content Include="' + fn + '" />\n' )
                f.write( '  </ItemGroup>\n' )

            if self.CompileFiles:
                f.write( '  <ItemGroup>\n' )
                for fn in [os.path.relpath(path, self.ProjectHome) for path in sorted(self.CompileFiles,key=str.lower) ]:
                    f.write( '    <Compile Include="' + fn + '" />\n' )
                f.write( '  </ItemGroup>\n' )

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

                f.write( '  <ItemGroup>\n' )
                for fn in sorted(directories):
                    f.write( '    <Folder Include="' + fn + '" />\n' )
                f.write( '  </ItemGroup>\n' )

            if self.VirtualEnvironments:
                f.write( '  <ItemGroup>\n')
                for venv in self.VirtualEnvironments:
                    f.write( '    <Interpreter Include="{0}">\n'.format(os.path.relpath(venv.Path, self.ProjectHome)))
                    f.write( '      <Id>{{{0}}}</Id>\n'.format(str(venv.GUID).upper()))
                    f.write( '      <BaseInterpreter>{{{0}}}</BaseInterpreter>\n'.format(str(venv.BaseInterpreter).upper()))
                    f.write( '      <Version>{0}</Version>\n'.format(venv.Version))
                    f.write( '      <Description>{0}</Description>\n'.format(venv.Description))
                    f.write( '      <InterpreterPath>{0}</InterpreterPath>\n'.format(venv.InterpreterPath))
                    f.write( '      <WindowsInterpreterPath>{0}</WindowsInterpreterPath>\n'.format(venv.WindowsInterpreterPath))
                    f.write( '      <LibraryPath>{0}</LibraryPath>\n'.format(venv.LibraryPath))
                    f.write( '      <PathEnvironmentVariable>{0}</PathEnvironmentVariable>\n'.format(venv.PathEnvironmentVariable))
                    f.write( '      <Architecture>{0}</Architecture>\n'.format(venv.Architecture))
                    f.write( '    </Interpreter>\n')
                f.write( '  </ItemGroup>\n' )

            if self.PythonInterpreters:
                f.write( '  <ItemGroup>\n')
                for interpreter in self.PythonInterpreters:
                    f.write( '    <InterpreterReference Include="{{{0}}}\\{1}" />\n'.format(str(interpreter.BaseInterpreter).upper(), interpreter.Version))
                f.write( '  </ItemGroup>\n' )

            f.write( '  <Import Project="$(PtvsTargetsFile)" Condition="Exists($(PtvsTargetsFile))" />\n')
            f.write( '  <Import Project="$(MSBuildToolsPath)\Microsoft.Common.targets" Condition="!Exists($(PtvsTargetsFile))" />\n')
            f.write( '</Project>' )
