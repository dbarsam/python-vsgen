# -*- coding: utf-8 -*-
"""
This module provides the necessary definitions to generate a Python Interpreter object.
"""

import os
import csv
import fnmatch
import uuid
    
class PymakeInterpreter(object):
    """
    PymakeInterpreter encapsulates the logic and data used to describe a Python interpreter or virtual environments

    :ivar GUID:                    The GUID of the Python Interpreter; if not provided one is generated automatically.
    :ivar BaseInterpreter:         The GUID of the base Python Interpreter (different if PymakeInterpreter is Virtual Environment); if not provided the value is self.GUID
    :ivar Architecture:            The architecture (either x86 or x64). if not provide the value is "".
    :ivar Version:                 The major.minor version string; if not provide the value is "".
    :ivar Description:             The human readable description string; if not provide the value is ""
    :ivar Path:                    The absolute path of the 'python.exe'; if not provide the value is ""
    :ivar InterpreterPath:         The relative path to self.Path of the 'python.exe'; if not provide the value is ""
    :ivar WindowsInterpreterPath:  The relative path to self.Path of the 'pythonw.exe'; if not provide the value is ""
    :ivar LibraryPath:             The relative path to self.Path of the 'Lib' folder that is part of the python.exe distribution; if not provide the value is "".
    :ivar PathEnvironmentVariable: The name of the Environment variable to be uses as PYTHONPATH; if not provide the value is "".
    """
    
    #: A CSV file contains the values of an environment
    EnvDefintionFile = 'PTVSEnvironment.csv'

    def __init__(self, **kwargs):
        """
        Constructor.

        :param **kwargs:         List of arbitrary keyworded arguments to be processed as instance variable data
        """
        super(PymakeInterpreter, self).__init__()
        self._import(kwargs)

    @staticmethod
    def from_directory(directory):
        """
        Creates one or more PymakeInterpreter(s) from all PTVSEnvironment.csv files recursively found in the directory.

        :param directory: The absolute path to the root directory.
        :return           List of PymakeInterpreter instances; an empty list otherwise.
        """
        interpreters = []
        for root, dirnames, filenames in os.walk(directory):
            for filename in fnmatch.filter(filenames, PymakeInterpreter.EnvDefintionFile):
                interpreters.extend( PymakeInterpreter.from_file(os.path.join(root, filename)))
        return interpreters
    
    @staticmethod
    def from_file(filename):
        """
        Creates one or more PymakeInterpreter(s) from a single PTVSEnvironment.csv file.

        :param filename:  The absolute path to the PTVSEnvironment.csv file.
        :return           List of PymakeInterpreter instances; an empty list otherwise.
        """
        interpreters = []
        try:
            with open(filename, 'rb') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')            
                for line in reader:
                    line['Path'] = os.path.dirname(filename)
                    interpreters.append(PymakeInterpreter(**line))
        except IOError:
            pass

        return interpreters

    def _import(self, datadict):
        """
        Internal method to import instance variables data from a dictionary. 

        :param datadict: The dictionary containing variables values.
        """
        self.GUID                       = datadict.get('Id', uuid.uuid1())
        self.BaseInterpreter            = datadict.get('BaseInterpreter', self.GUID)
        self.Architecture               = datadict.get('Architecture', "")
        self.Version                    = datadict.get('Version', "")
        self.Path                       = datadict.get('Path', "")
        self.Description                = datadict.get('Description', "")
        self.InterpreterPath            = datadict.get('InterpreterPath', "")
        self.InterpreterAbsPath         = datadict.get('InterpreterAbsPath', self.InterpreterPath if os.path.isabs(self.InterpreterPath) else os.path.abspath(os.path.join(self.Path, self.InterpreterPath)))
        self.WindowsInterpreterPath     = datadict.get('WindowsInterpreterPath', "")
        self.WindowsInterpreterAbsPath  = datadict.get('WindowsInterpreterAbsPath', self.WindowsInterpreterPath if os.path.isabs(self.WindowsInterpreterPath) else os.path.abspath(os.path.join(self.Path, self.WindowsInterpreterPath)))
        self.LibraryPath                = datadict.get('LibraryPath', "")
        self.LibraryAbsPath             = datadict.get('LibraryAbsPath', self.LibraryPath if os.path.isabs(self.LibraryPath) else os.path.abspath(os.path.join(self.Path, self.LibraryPath)))
        self.PathEnvironmentVariable    = datadict.get('PathEnvironmentVariable', "")

    def register(self):
        """
        'Registers' the environment into the windows registry.

        :..note: https://pytools.codeplex.com/workitem/2765
        """
        import os
        import _winreg
        regkey_name = r'Software\Microsoft\VisualStudio\11.0\PythonTools\Interpreters\{{{0}}}'.format(str(self.GUID).lower())
        try:
            regkey = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER, regkey_name)
            _winreg.SetValueEx(regkey, 'Architecture', 0, _winreg.REG_SZ, self.Architecture)
            _winreg.SetValueEx(regkey, 'Description', 0, _winreg.REG_SZ, self.Description)
            _winreg.SetValueEx(regkey, 'InterpreterPath', 0, _winreg.REG_SZ, self.InterpreterAbsPath)
            _winreg.SetValueEx(regkey, 'LibraryPath', 0, _winreg.REG_SZ, self.LibraryAbsPath)
            _winreg.SetValueEx(regkey, 'PathEnvironmentVariable', 0, _winreg.REG_SZ, self.PathEnvironmentVariable)
            _winreg.SetValueEx(regkey, 'Version', 0, _winreg.REG_SZ, self.Version)
            _winreg.SetValueEx(regkey, 'WindowsInterpreterPath', 0, _winreg.REG_SZ, self.WindowsInterpreterAbsPath)
            _winreg.SetValueEx(regkey, 'PathEnvironmentVariable', 0, _winreg.REG_SZ, self.PathEnvironmentVariable)
            _winreg.CloseKey(regkey)
        except WindowsError as ex:
            return False
        return True
