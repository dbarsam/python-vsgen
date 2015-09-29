# -*- coding: utf-8 -*-
"""
This module provides the necessary definitions to generate a Python Interpreter object.
"""

import os
import csv
import fnmatch
import uuid
import subprocess
try:
    import winreg
except ImportError:
    import _winreg as winreg
from pymake.register import PyRegisterable

class PymakeInterpreter(PyRegisterable):
    """
    PymakeInterpreter encapsulates the logic and data used to describe a Python interpreter or virtual environments

    :ivar GUID:                    The GUID of the Python Interpreter; if not provided one is generated automatically.
    :ivar BaseInterpreter:         The GUID of the base Python Interpreter (different if PymakeInterpreter is Virtual Environment); if not provided the value is self.GUID
    :ivar Architecture:            The architecture (either x86 or Amd64). if not provide the value is "".
    :ivar Version:                 The major.minor version string; if not provide the value is "".
    :ivar Description:             The human readable description string; if not provide the value is ""
    :ivar Path:                    The absolute path of the 'python.exe'; if not provide the value is ""
    :ivar InterpreterPath:         The relative path to self.Path of the 'python.exe'; if not provide the value is ""
    :ivar WindowsInterpreterPath:  The relative path to self.Path of the 'pythonw.exe'; if not provide the value is ""
    :ivar LibraryPath:             The relative path to self.Path of the 'Lib' folder that is part of the python.exe distribution; if not provide the value is "".
    :ivar PathEnvironmentVariable: The name of the Environment variable to be uses as PYTHONPATH; if not provide the value is "".
    """
    __registerable_name__ = "Python Interpreter"

    #: PTVS Interpreter Register Location
    regkey_name = r'Software\Microsoft\VisualStudio\{VSVersion}\PythonTools\Interpreters'

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
        :return           A valid PymakeInterpreter instance if succesful; None otherwise.
        """
        interpreters = []
        for root, dirnames, filenames in os.walk(directory):
            for filename in fnmatch.filter(filenames, PymakeInterpreter.EnvDefintionFile):
                interpreters.extend( PymakeInterpreter.from_file(os.path.join(root, filename)))
        return interpreters
    
    @staticmethod
    def from_virtual_environment(directory, **kwargs):
        """
        Creates a PymakeInterpreter from an Python Virtual Environment in the directory.

        :param directory: The absolute path to the python installation directory.
        :param **kwargs:  List of additional keyworded arguments to be passed into the PymakeInterpreter.
        :return           A valid PymakeInterpreter instance if succesful; None otherwise.
        """
        root = os.path.abspath(directory)
        python = os.path.abspath(os.path.join(root, 'Scripts', 'python.exe'))
        if not os.path.exists(python):
            return None

        root = os.path.abspath(directory)
        origprefix = os.path.abspath(os.path.join(root, 'Lib', 'orig-prefix.txt'))
        if not os.path.exists(origprefix):
            return None
        
        with open(origprefix, 'rt') as f:
            basedir = next((line.rstrip() for line in f), None)
            baseinterpretter = PymakeInterpreter.from_python_installation(basedir,  **kwargs)
        if not baseinterpretter:
            return None

        args = kwargs.copy()
        args['Path'] = root
        args['BaseInterpreter'] = baseinterpretter.GUID
        args['InterpreterPath'] = os.path.join('Scripts', 'python.exe')
        args.setdefault('Description', '{} ({})'.format(os.path.basename(root), baseinterpretter.Description))

        if os.path.exists(os.path.join(root, 'Scripts', 'pythonw.exe')):
            args['WindowsInterpreterPath'] = os.path.join('Scripts', 'pythonw.exe')

        if os.path.exists(os.path.join(root, 'Lib')):
            args['LibraryPath'] = 'Lib\\'

        try:
            out, err = subprocess.Popen([python, '-c', 'import sys;print ".".join(str(s) for s in sys.version_info[:2])'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            args['Version'] = out.decode("utf-8").rstrip()
        except Exception as e:
            pass

        try:
            out, err = subprocess.Popen([python, '-c', 'import platform; print "Amd64" if "64bit" in platform.architecture() else "x86"'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            args['Architecture'] = out.decode("utf-8").rstrip()
        except Exception:
            pass

        interpreter = PymakeInterpreter(**args)
        return interpreter

    @staticmethod
    def from_python_installation(directory, **kwargs):
        """
        Creates a PymakeInterpreter from an Python Installation in the directory.

        :param directory: The absolute path to the python installation directory.
        :param **kwargs:  List of additional keyworded arguments to be passed into the PymakeInterpreter.
        :return           A valid PymakeInterpreter instance if succesful; None otherwise.
        """
        root = os.path.abspath(directory)
        python = os.path.abspath(os.path.join(root, 'python.exe'))
        if not os.path.exists(python):
            return None
        
        args = kwargs.copy()
        args['Path'] = root
        args['InterpreterPath'] = 'python.exe'
        args.setdefault('Description', os.path.basename(root))

        if os.path.exists(os.path.join(root, 'pythonw.exe')):
            args['WindowsInterpreterPath'] = 'pythonw.exe'

        if os.path.exists(os.path.join(root, 'Lib')):
            args['LibraryPath'] = 'Lib\\'

        try:
            out, err = subprocess.Popen([python, '-c', 'import sys;print ".".join(str(s) for s in sys.version_info[:2])'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            args['Version'] = out.decode("utf-8").rstrip()
        except Exception as e:
            pass

        try:
            out, err = subprocess.Popen([python, '-c', 'import platform; print "Amd64" if "64bit" in platform.architecture() else "x86"'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            args['Architecture'] = out.decode("utf-8").rstrip()
        except Exception:
            pass

        interpreter = PymakeInterpreter(**args)
        interpreter.resolve()
        return interpreter

    @staticmethod
    def from_file(filename):
        """
        Creates one or more PymakeInterpreter(s) from a single PTVSEnvironment.csv file.

        :param filename:  The absolute path to the PTVSEnvironment.csv file.
        :return           List of PymakeInterpreter instances; an empty list otherwise.
        """
        interpreters = []
        try:
            with open(filename, 'rt') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')            
                for line in reader:
                    line['Path'] = os.path.dirname(filename)
                    interpreters.append(PymakeInterpreter(**line))
        except IOError:
            pass

        return interpreters

    @staticmethod
    def from_registry_key(keyname):
        """
        Creates a PymakeInterpreter from a single registry key.

        :param keyname:  The keyname under HKEY_CURRENT_USER referring to the environment.       
        :return:         A valid PymakeInterpreter instance if succesful; None otherwise.
        """
        args = {}
        try:
            regkey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, keyname)
            for k in ['Architecture', 'Description', 'InterpreterPath', 'LibraryPath', 'PathEnvironmentVariable', 'Version', 'WindowsInterpreterPath', 'PathEnvironmentVariable']:
                args[k] = winreg.QueryValueEx(regkey, k)[0]        
            winreg.CloseKey(regkey)
        except WindowsError as ex:
            pass

        if 'InterpreterPath' in args:
            args['Path'] = os.path.dirname(args['InterpreterPath'])
            args['Id'] = os.path.basename(keyname)[1:-1]
            return PymakeInterpreter(**args) 
        return None

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
        self.VSVersion                  = datadict.get('VSVersion', None)

    def resolve(self):
        """
        'Resolves' the environment with existing environments in the windows registry.
        """
        if not self.VSVersion:
            raise ValueError('Cannot resolve interpreter with invalid Visual Studio Version')

        regkey_name = self.regkey_name.format(VSVersion=self.VSVersion)
        try:
            vs_regkey_name = os.path.dirname(regkey_name)
            winreg.OpenKey(winreg.HKEY_CURRENT_USER, vs_regkey_name)
        except WindowsError as ex:
            raise ValueError('Cannot resolve interpreter with Visual Studio %s that is not installed.' % str(self.VSVersion))

        regkey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, regkey_name)
        try:
            reginfo = winreg.QueryInfoKey(regkey)
            for i in range(reginfo[0]):
                interpreter_regkey_name = '{0}\\{1}'.format(regkey_name, winreg.EnumKey(regkey, i))
                interpreter = PymakeInterpreter.from_registry_key(interpreter_regkey_name)
                if interpreter and interpreter.InterpreterAbsPath == self.InterpreterAbsPath:
                    self.GUID = uuid.UUID(interpreter.GUID)
                    self.BaseInterpreter = self.GUID
                    break
        except WindowsError as ex:
            pass

    def register(self):
        """
        'Registers' the environment into the windows registry.

        :..note: https://pytools.codeplex.com/workitem/2765
        """
        if not self.VSVersion:
            raise ValueError('Cannot register interpreter with invalid Visual Studio Version')

        regkey_name = self.regkey_name.format(VSVersion=self.VSVersion)
        try:
            vs_regkey_name = os.path.dirname(regkey_name)
            winreg.OpenKey(winreg.HKEY_CURRENT_USER, vs_regkey_name)
        except WindowsError as ex:
            raise ValueError('Cannot register interpreter with Visual Studio %s that is not installed.' % str(self.VSVersion))

        interpreter_regkey_name = '{0}\\{{{1}}}'.format(regkey_name, str(self.GUID).lower())
        try:
            regkey = winreg.CreateKey(winreg.HKEY_CURRENT_USER, interpreter_regkey_name)
            winreg.SetValueEx(regkey, 'Architecture', 0, winreg.REG_SZ, self.Architecture)
            winreg.SetValueEx(regkey, 'Description', 0, winreg.REG_SZ, self.Description)
            winreg.SetValueEx(regkey, 'InterpreterPath', 0, winreg.REG_SZ, self.InterpreterAbsPath)
            winreg.SetValueEx(regkey, 'LibraryPath', 0, winreg.REG_SZ, self.LibraryAbsPath)
            winreg.SetValueEx(regkey, 'PathEnvironmentVariable', 0, winreg.REG_SZ, self.PathEnvironmentVariable)
            winreg.SetValueEx(regkey, 'Version', 0, winreg.REG_SZ, self.Version)
            winreg.SetValueEx(regkey, 'WindowsInterpreterPath', 0, winreg.REG_SZ, self.WindowsInterpreterAbsPath)
            winreg.SetValueEx(regkey, 'PathEnvironmentVariable', 0, winreg.REG_SZ, self.PathEnvironmentVariable)
            winreg.CloseKey(regkey)
        except WindowsError as ex:
            return False
        return True
