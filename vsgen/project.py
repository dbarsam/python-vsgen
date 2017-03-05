# -*- coding: utf-8 -*-
"""
This module provides the neccessary defintions to support a base project file defintion.
"""

import os
import csv
import fnmatch
import uuid

from vsgen.writer import VSGWritable
from vsgen.register import VSGRegisterable


class VSGProject(VSGWritable, VSGRegisterable):
    """
    VSGProject encapsulates the data and logic needed to act as a base project.

    :ivar uuid  GUID:                   The GUID of the project; if not provided one is generated automatically.
    :ivar str   FileName:               The absolute filename of the project file; if not provided the value is ""
    :ivar str   Name:                   The display name of the project; if not provide the value is "".
    :ivar str   WorkingDirectory:       The absolute directory that will be the working directory of the project; if not provide the value is ""
    :ivar str   OutputPath:             The absolute directory that will be the output directory of the project; if not provide the value is "".
    :ivar str   RootNamespace:          The name of the root namespace of the project; if not provide the value is "". `Ignored`.
    :ivar str   ProjectHome:            The absolute directory of the project's source root folder; if not provide the value is ""
    :ivar str   StartupFile:            The absolute path to the Startup file; if not provide the value is ""
    :ivar list  CompileFiles:           The list of absolute files that will comprise the projects compile group; if not provide the value is [].
    :ivar list  ContentFiles:           The list of absolute files that will comprise the projects content group; if not provide the value is [].
    :ivar list  Directories:            The list of absolute directories that will comprise the projects directory group; if not provide the value is [].
    :ivar list  DirectoryInFilter:      A list of fnmatch expressions to match directories to be included during the item generation step; if not provided the value is [].
    :ivar list  DirectoryExFilter:      A list of fnmatch expressions to match directories to be excludes during the item generation step; if not provided the value is [].
    :ivar list  CompileInFilter:        A list of fnmatch expressions to match compile files to be included during the item generation step; if not provide the value is [].
    :ivar list  CompileExFilter:        A list of fnmatch expressions to match compile files to be excluded during the item generation step; if not provide the value is [].
    :ivar list  ContentInFilter:        A list of fnmatch expressions to match content files to be included during the item generation step; if not provide the value is [].
    :ivar list  ContentExFilter:        A list of fnmatch expressions to match content files to be excluded during the item generation step; if not provide the value is [].
    :ivar float VSVersion:              The Visual Studio version; if not provide the value is ``None``.
    """
    __project_type__ = None

    __writable_name__ = "Visual Studio Base Project"

    __registerable_name__ = "Visual Studio Base Registerable"

    def __init__(self, **kwargs):
        """
        Constructor.

        :param kwargs:         List of arbitrary keyworded arguments to be processed as instance variable data
        """
        super(VSGProject, self).__init__()
        self._import(kwargs)

    def _import(self, datadict):
        """
        Internal method to import instance variables data from a dictionary

        :param dict datadict: The dictionary containing variables values.
        """
        self.GUID = datadict.get("GUID", uuid.uuid1())
        self.FileName = datadict.get("FileName", "")
        self.Name = datadict.get("Name", "")
        self.WorkingDirectory = datadict.get("WorkingDirectory", "")
        self.OutputPath = datadict.get("OutputPath", "")
        self.RootNamespace = datadict.get("RootNamespace", "")
        self.ProjectHome = datadict.get("ProjectHome", "")
        self.StartupFile = datadict.get("StartupFile", "")
        self.CompileFiles = datadict.get("CompileFiles", [])
        self.ContentFiles = datadict.get("ContentFiles", [])
        self.Directories = datadict.get("Directories", [])
        self.DirectoryInFilter = datadict.get("DirectoryInFilter", [])
        self.DirectoryExFilter = datadict.get("DirectoryExFilter", [])
        self.CompileInFilter = datadict.get("CompileInFilter", [])
        self.CompileExFilter = datadict.get("CompileExFilter", [])
        self.ContentInFilter = datadict.get("ContentInFilter", [])
        self.ContentExFilter = datadict.get("ContentExFilter", [])
        self.VSVersion = datadict.get("VSVersion", None)

    @classmethod
    def from_section(cls, config, section, **kwargs):
        """
        Creates a :class:`~vsgen.project.VSGProject` from a :class:`~configparser.ConfigParser` section.

        :param ConfigParser config:   A :class:`~configparser.ConfigParser` instance.
        :param str          section:  A :class:`~configparser.ConfigParser` section key.
        :param              kwargs:   List of additional keyworded arguments to be passed into the :class:`~vsgen.project.VSGProject`.
        :return:                      A valid :class:`~vsgen.project.VSGProject` instance if succesful; None otherwise.
        """
        p = cls(**kwargs)

        p.Name = config.get(section, 'name', fallback=p.Name)
        p.FileName = config.getfile(section, 'filename', fallback=p.FileName)
        p.SearchPath = config.getdirs(section, 'search_path', fallback=p.SearchPath)
        p.OutputPath = config.getdir(section, 'output_path', fallback=p.OutputPath)
        p.WorkingDirectory = config.getdir(section, 'working_directory', fallback=p.WorkingDirectory)
        p.RootNamespace = config.get(section, 'root_namespace', fallback=p.RootNamespace)
        p.ProjectHome = config.getdir(section, 'project_home', fallback=p.ProjectHome)
        p.StartupFile = config.getfile(section, 'startup_file', fallback=p.StartupFile)
        p.CompileFiles = config.getlist(section, 'compile_files', fallback=p.CompileFiles)
        p.ContentFiles = config.getlist(section, 'content_files', fallback=p.ContentFiles)
        p.CompileInFilter = config.getlist(section, 'compile_in_filter', fallback=p.CompileInFilter)
        p.CompileExFilter = config.getlist(section, 'compile_ex_filter', fallback=p.CompileExFilter)
        p.ContentInFilter = config.getlist(section, 'content_in_filter', fallback=p.ContentInFilter)
        p.ContentExFilter = config.getlist(section, 'content_ex_filter', fallback=p.ContentExFilter)
        p.DirectoryInFilter = config.getlist(section, 'directory_in_filter', fallback=p.DirectoryInFilter)
        p.DirectoryExFilter = config.getlist(section, 'directory_ex_filter', fallback=p.DirectoryExFilter)

        root_path = config.get(section, 'root_path', fallback="")
        p.insert_files(root_path)

        return p

    def insert_files(self, rootpath, directoryInFilter=None, directoryExFilter=None, compileInFilter=None, compileExFilter=None, contentInFilter=None, contentExFilter=None):
        """
        Inserts files by recursive traversing the rootpath and inserting files according the addition filter parameters.

        :param str rootpath:            The absolute path to the root directory.
        :param list directoryInFilter:  A list of fnmatch expressions to match directories to be included.  A `None` value will default to :attr:`DirectoryInFilter`.
        :param list directoryExFilter:  A list of fnmatch expressions to match directories to be excluded.  A `None` value will default to :attr:`DirectoryExFilter`.
        :param list compileInFilter:    A list of fnmatch expressions to match compile files to be included.  A `None` value will default to :attr:`CompileInFilter`.
        :param list compileExFilter:    A list of fnmatch expressions to match compile files to be excludes.  A `None` value will default to :attr:`CompileExFilter`.
        :param list contentInFilter:    A list of fnmatch expressions to match content files to be includes.  A `None` value will default to :attr:`ContentInFilter`.
        :param list contentExFilter:    A list of fnmatch expressions to match content files to be excludes.  A `None` value will default to :attr:`ContentExFilter`.
        """
        # Overrides
        directoryInFilter = self.DirectoryInFilter if directoryInFilter is None else directoryInFilter
        directoryExFilter = self.DirectoryExFilter if directoryExFilter is None else directoryExFilter
        compileInFilter = self.CompileInFilter if compileInFilter is None else compileInFilter
        compileExFilter = self.CompileExFilter if compileExFilter is None else compileExFilter
        contentInFilter = self.ContentInFilter if contentInFilter is None else contentInFilter
        contentExFilter = self.ContentExFilter if contentExFilter is None else contentExFilter

        def filter(text, filters, explicit):
            """
            Convience filter function

            :param text text: The target text.
            :param list filters: The collection of fnmatch expressions
            :param bool explicit: Flag denoting an the empty filter collection return match failure.
            """
            if explicit:
                return any(fnmatch.fnmatch(text, f) for f in filters)
            return not filters or any(fnmatch.fnmatch(text, f) for f in filters)

        for root, dirnames, filenames in os.walk(rootpath):

            searchdir = os.path.normpath(os.path.normcase(root))

            # If the root dir matches an excluded directory, stop any further searches
            if filter(searchdir, directoryExFilter, True):
                dirnames[:] = []
            elif filter(searchdir, directoryInFilter, False):
                for filepath in [os.path.join(root, filename) for filename in filenames]:
                    if filter(filepath, compileInFilter, False) and not filter(filepath, compileExFilter, True):
                        self.CompileFiles.append(filepath)
                    elif filter(filepath, contentInFilter, False) and not filter(filepath, contentExFilter, True):
                        self.ContentFiles.append(filepath)

    def write(self):
        """
        Creates the project file.
        """
        raise NotImplementedError('{}.write() method not implemented.'.format(self.__class__))

    def register(self):
        """
        Registers the project components.
        """
        raise NotImplementedError('{}.register() method not implemented.'.format(self.__class__))
