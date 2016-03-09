# -*- coding: utf-8 -*-
"""
This module provides the necessary definitions to generate a Python Interpreter object.
"""

import os
import re
import csv
import site
import fnmatch
import uuid
import subprocess
import configparser
try:
    import winreg
except ImportError:
    import _winreg as winreg
from vsgen.register import VSGRegisterable


class PTVSInterpreter(VSGRegisterable):
    """
    PTVSInterpreter encapsulates the logic and data used to describe a Python interpreter or virtual environments

    :ivar uuid GUID:                    The GUID of the Python Interpreter; if not provided one is generated automatically.
    :ivar uuid BaseInterpreter:         The GUID of the base Python Interpreter (different if PTVSInterpreter is Virtual Environment); if not provided the value is :attr:`GUID`
    :ivar str  Architecture:            The architecture (either x86 or Amd64). if not provide the value is "".
    :ivar str  Version:                 The major.minor version string; if not provide the value is "".
    :ivar str  Description:             The human readable description string; if not provide the value is ""
    :ivar str  Path:                    The absolute path of the `python.exe`; if not provide the value is ""
    :ivar str  InterpreterPath:         The relative path to self.Path of the `python.exe`; if not provide the value is ""
    :ivar str  WindowsInterpreterPath:  The relative path to self.Path of the `pythonw.exe`; if not provide the value is ""
    :ivar str  LibraryPath:             The relative path to self.Path of the `Lib` folder that is part of the python.exe distribution; if not provide the value is "".
    :ivar str  PathEnvironmentVariable: The name of the environment variable to be uses as `PYTHONPATH`; if not provide the value is "PYTHONPATH".
    """
    __registerable_name__ = "Python Interpreter"

    #: PTVS Interpreter Registry Location
    _regkey_name = r'Software\Microsoft\VisualStudio\{VSVersion}\PythonTools\Interpreters'

    def __init__(self, **kwargs):
        """
        Constructor.

        :param kwargs:         List of arbitrary keyworded arguments to be processed as instance variable data
        """
        super(PTVSInterpreter, self).__init__()
        self._import(kwargs)

    @classmethod
    def from_section(cls, config, section, **kwargs):
        """
        Creates a :class:`~vsgen.ptvs.interpreter.PTVSInterpreter` from a :class:`~configparser.ConfigParser` section.

        :param obj config:   A :class:`~configparser.ConfigParser` instance.
        :param str section:  A :class:`~configparser.ConfigParser` section key.
        :param kwargs:       List of additional keyworded arguments to be passed into the :class:`~vsgen.ptvs.interpreter.PTVSInterpreter`.
        :return:             A valid :class:`~vsgen.ptvs.interpreter.PTVSInterpreter` instance if succesful; None otherwise.
        """
        if section not in config:
            raise ValueError('Section [{}] not found in [{}]'.format(section, ', '.join(config.sections())))

        interpreters = []
        interpreter_paths = config.getdirs(section, 'interpreter_paths', fallback=[])
        if interpreter_paths:
            interpreters.extend([PTVSInterpreter.from_python_installation(p, **kwargs) for p in interpreter_paths])

        environment_paths = config.getdirs(section, 'environment_paths', fallback=[])
        if environment_paths:
            interpreters = [PTVSInterpreter.from_virtual_environment(p, **kwargs) for p in environment_paths]

        for i in interpreters:
            i.Description = config.get(section, 'description', fallback=i.Description)

        return interpreters

    @classmethod
    def from_virtual_environment(cls, directory, **kwargs):
        """
        Creates a :class:`~vsgen.ptvs.interpreter.PTVSInterpreter` from an Python Virtual Environment in the directory.

        :param str directory: The absolute path to the python virtual environment directory.
        :param kwargs:    List of additional keyworded arguments to be passed into the :class:`~vsgen.ptvs.interpreter.PTVSInterpreter`.
        :return:          A valid :class:`~vsgen.ptvs.interpreter.PTVSInterpreter` instance if succesful; None otherwise.
        """
        root = os.path.abspath(directory)
        python = os.path.abspath(os.path.join(root, 'Scripts', 'python.exe'))
        if not os.path.exists(python):
            return None

        root = os.path.abspath(directory)
        origprefix = os.path.abspath(os.path.join(root, 'Lib', 'orig-prefix.txt'))
        pyvenvcfg = os.path.abspath(os.path.join(root, 'pyvenv.cfg'))
        if not os.path.exists(origprefix) and not os.path.exists(pyvenvcfg):
            return None

        if os.path.exists(origprefix):
            with open(origprefix, 'rt') as f:
                basedir = next((line.rstrip() for line in f), None)

        if os.path.exists(pyvenvcfg):
            config_line = re.compile(site.CONFIG_LINE)
            with open(pyvenvcfg, encoding='utf-8') as f:
                for line in f:
                    m = config_line.match(line.rstrip())
                    if m:
                        d = m.groupdict()
                        key, value = d['key'].lower(), d['value']
                        if key == 'home':
                            basedir = value

        baseinterpretter = cls.from_python_installation(basedir, **kwargs)
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

        interpreter = cls(**args)
        return interpreter

    @classmethod
    def from_python_installation(cls, directory, **kwargs):
        """
        Creates a :class:`~vsgen.ptvs.interpreter.PTVSInterpreter` from an Python installation in the directory.

        :param str directory: The absolute path to the python installation directory.
        :param kwargs:  List of additional keyworded arguments to be passed into the :class:`~vsgen.ptvs.interpreter.PTVSInterpreter`.
        :return:          A valid :class:`~vsgen.ptvs.interpreter.PTVSInterpreter` instance if succesful; None otherwise.
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

        interpreter = cls(**args)
        interpreter.resolve()
        return interpreter

    @classmethod
    def from_registry_key(cls, keyname):
        """
        Creates a :class:`~vsgen.ptvs.interpreter.PTVSInterpreter` from a single registry key.

        :param str keyname:  The keyname under `HKEY_CURRENT_USER` referring to the environment.
        :return:         A valid :class:`~vsgen.ptvs.interpreter.PTVSInterpreter` instance if succesful; None otherwise.
        """
        args = {}
        try:
            regkey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, keyname)
            for k in ['Architecture', 'Description', 'InterpreterPath', 'LibraryPath', 'PathEnvironmentVariable', 'Version', 'WindowsInterpreterPath']:
                args[k] = winreg.QueryValueEx(regkey, k)[0]
            winreg.CloseKey(regkey)
        except WindowsError as ex:
            pass

        if 'InterpreterPath' in args:
            args['Path'] = os.path.dirname(args['InterpreterPath'])
            args['Id'] = os.path.basename(keyname)[1:-1]
            return cls(**args)
        return None

    def _import(self, datadict):
        """
        Internal method to import instance variables data from a dictionary.

        :param dict datadict: The dictionary containing variables values.
        """
        self.GUID = datadict.get('Id', uuid.uuid1())
        self.BaseInterpreter = datadict.get('BaseInterpreter', self.GUID)
        self.Architecture = datadict.get('Architecture', "")
        self.Version = datadict.get('Version', "")
        self.Path = datadict.get('Path', "")
        self.Description = datadict.get('Description', "")
        self.InterpreterPath = datadict.get('InterpreterPath', "")
        self.InterpreterAbsPath = datadict.get('InterpreterAbsPath', self.InterpreterPath if os.path.isabs(self.InterpreterPath) else os.path.abspath(os.path.join(self.Path, self.InterpreterPath)))
        self.WindowsInterpreterPath = datadict.get('WindowsInterpreterPath', "")
        self.WindowsInterpreterAbsPath = datadict.get('WindowsInterpreterAbsPath', self.WindowsInterpreterPath if os.path.isabs(self.WindowsInterpreterPath) else os.path.abspath(os.path.join(self.Path, self.WindowsInterpreterPath)))
        self.LibraryPath = datadict.get('LibraryPath', "")
        self.LibraryAbsPath = datadict.get('LibraryAbsPath', self.LibraryPath if os.path.isabs(self.LibraryPath) else os.path.abspath(os.path.join(self.Path, self.LibraryPath)))
        self.PathEnvironmentVariable = datadict.get('PathEnvironmentVariable', "PYTHONPATH")
        self.VSVersion = datadict.get('VSVersion', None)

    def resolve(self):
        """
        Resolves the environment with one already existing in the windows registry.

        :note: We're explictly writing the environment to the registry to facilitate sharing so to avoid duplication we try to match the environment to an existing one first.
        """
        if not self.VSVersion:
            raise ValueError('Cannot resolve interpreter with invalid Visual Studio Version')

        regkey_name = self._regkey_name.format(VSVersion=self.VSVersion)
        try:
            vs_regkey_name = os.path.dirname(regkey_name)
            winreg.OpenKey(winreg.HKEY_CURRENT_USER, vs_regkey_name)
        except WindowsError as ex:
            raise ValueError('Cannot resolve the registry path HKCU\%s for Visual Studio %s\'s PTVS.  Is PTVS installed?' % (vs_regkey_name, self.text(self.VSVersion)))

        regkey = winreg.CreateKey(winreg.HKEY_CURRENT_USER, regkey_name)
        try:
            reginfo = winreg.QueryInfoKey(regkey)
            for i in range(reginfo[0]):
                interpreter_regkey_name = '{0}\\{1}'.format(regkey_name, winreg.EnumKey(regkey, i))
                interpreter = self.from_registry_key(interpreter_regkey_name)
                if interpreter and interpreter.InterpreterAbsPath.lower() == self.InterpreterAbsPath.lower():
                    self.GUID = uuid.UUID(interpreter.GUID)
                    self.BaseInterpreter = self.GUID
                    break
        except WindowsError as ex:
            pass

    def register(self):
        """
        Registers the environment into the windows registry.

        :note: We're explictly writing the environment to the registry to facilitate sharing. See `How to share pyproj across team with custom environments <https://pytools.codeplex.com/workitem/2765>`_ for motivation.
        """
        if not self.VSVersion:
            raise ValueError('Cannot register interpreter with invalid Visual Studio Version')

        regkey_name = self._regkey_name.format(VSVersion=self.VSVersion)
        try:
            vs_regkey_name = os.path.dirname(regkey_name)
            winreg.OpenKey(winreg.HKEY_CURRENT_USER, vs_regkey_name)
        except WindowsError as ex:
            raise ValueError('Cannot register interpreter with Visual Studio %s that is not installed.' % self.text(self.VSVersion))

        interpreter_regkey_name = '{0}\\{{{1}}}'.format(regkey_name, self.lower(self.GUID))
        try:
            regkey = winreg.CreateKey(winreg.HKEY_CURRENT_USER, interpreter_regkey_name)
            winreg.SetValueEx(regkey, 'Architecture', 0, winreg.REG_SZ, self.Architecture)
            winreg.SetValueEx(regkey, 'Description', 0, winreg.REG_SZ, self.Description)
            winreg.SetValueEx(regkey, 'InterpreterPath', 0, winreg.REG_SZ, self.InterpreterAbsPath)
            winreg.SetValueEx(regkey, 'LibraryPath', 0, winreg.REG_SZ, self.LibraryAbsPath)
            winreg.SetValueEx(regkey, 'Version', 0, winreg.REG_SZ, self.Version)
            winreg.SetValueEx(regkey, 'WindowsInterpreterPath', 0, winreg.REG_SZ, self.WindowsInterpreterAbsPath)
            winreg.SetValueEx(regkey, 'PathEnvironmentVariable', 0, winreg.REG_SZ, self.PathEnvironmentVariable)
            winreg.CloseKey(regkey)
        except WindowsError as ex:
            return False
        return True
