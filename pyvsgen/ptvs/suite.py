# -*- coding: utf-8 -*-
"""
This module provides all functionality for specializing Pyvsgen's suite class specific to PTVS projects.
"""
import os

from pyvsgen.ptvs.project import PTVSProject
from pyvsgen.ptvs.interpreter import PTVSInterpreter

def getproject( config, section, **kwargs):
    """
    Creates a Pyvsgen project from a configparser instance.

    :param obj config: The instance of the configparser class
    :param str section: The section name to read.
    :param **kwargs:  List of additional keyworded arguments to be passed into the PTVSProject.
    :return: A valid PTVSProject instance if succesful; None otherwise.
    """
    p = PTVSProject(**kwargs)
        
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
    p.DirectoryInFilter = config.getdirs(section, 'directory_in_filter', fallback=p.DirectoryInFilter)
    p.DirectoryExFilter = config.getdirs(section, 'directory_ex_filter', fallback=p.DirectoryExFilter)
    p.IsWindowsApplication =  config.getboolean(section, 'is_windows_application', fallback=p.IsWindowsApplication)
    p.PythonInterpreterArgs = config.getlist(section, 'python_interpreter_args', fallback=p.PythonInterpreterArgs)

    interpreter = config.get(section, 'python_interpreter', fallback=None)
    interpreters = {n:[i for i in getinterpreter(config, n, VSVersion=p.VSVersion)] for n in config.getlist(section, 'python_interpreters')}        
    p.PythonInterpreters = [i for v in interpreters.values() for i in v]
    p.PythonInterpreter = next((i for i in interpreters.get(interpreter, [])), None)

    virtual_environments = config.getlist(section, 'python_virtual_environments', fallback=[])
    p.VirtualEnvironments = [ve for n in virtual_environments for ve in getvirtualenvironment(config, n, VSVersion=p.VSVersion) ]

    root_path = config.get(section, 'root_path', fallback="")
    p.insert_files(root_path)

    return p

def getinterpreter(config, section, **kwargs):
    """
    Creates a Pyvsgen Interpreter from a configparser instance.

    :param obj config: The instance of the configparser class
    :param str section: The section name to read.
    :param **kwargs:  List of additional keyworded arguments to be passed into the PTVSInterpreter.
    :return: A valid PTVSInterpreter instance if succesful; None otherwise.
    """
    if section not in config:
        raise ValueError('Section [{}] not found in [{}]'.format(section, ', '.join(config.sections())))

    interpreters = []
    interpreter_paths = config.getdirs(section, 'interpreter_paths', fallback=[])
    if interpreter_paths:
        interpreters = [PTVSInterpreter.from_python_installation( p, **kwargs) for p in interpreter_paths]

    for i in interpreters:
        i.Description = config.get(section, 'description', fallback=i.Description)
    
    return interpreters

def getvirtualenvironment(config, section, **kwargs):
    """
    Creates a Pyvsgen Interpreter (Virtual Environment) from a configparser instance.

    :param obj config: The instance of the configparser class
    :param str section: The section name to read.
    :param **kwargs:  List of additional keyworded arguments to be passed into the PTVSInterpreter.
    :return: A valid PTVSInterpreter instance if succesful; None otherwise.
    """
    if section not in config:
        raise ValueError('Section [{}] not found in [{}]'.format(section, ', '.join(config.sections())))
    
    environments = []
    environment_paths = config.getdirs(section, 'environment_paths', fallback=[])
    if environment_paths:
        environments = [PTVSInterpreter.from_virtual_environment( p, **kwargs ) for p in environment_paths]

    for e in environments:
        e.Description = config.get(section, 'description', fallback=e.Description)

    return environments
