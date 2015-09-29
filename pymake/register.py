# -*- coding: utf-8 -*-
"""
This module provides a simple register utility for Pymake objects.
"""
import time

class PyRegisterable(object):
    """
    An interface class defining methods necessary for PyRegisterable
    """
    __resgisterable_name__ = "Unknown Resgisterable"

    def register( self ):
        raise NotImplementedError( "Should have implemented this" )

class PyRegisterCommand(object):
    """
    The PyRegisterCommand class presents a simple command object to execute the register methods of a collection of PyRegisterable objects.
    """
    def __init__(self, logname, registerables):
        """
        Initializes the instance with an collection of registerables.

        :param str logname:  The python logger log name.
        :param list registerables:  The list of PyRegisterable class instances.
        """
        self._logname = logname
        self._registerables = registerables
        registerables_names = set([r.__registerable_name__ for r in registerables])
        if not registerables_names:
            self._message = "Registering no files."
        elif len(registerables_names) == 1:
            self._message = "Registering {0}{1}".format(next(iter(registerables_names)), 's' if len(registerables) > 1 else '')
        else:
            self._message = "Registering a mixed collection of files."

    def __enter__(self):
        """
        Enter the runtime context related to this object.
        """
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """
        Exit the runtime context related to this object.
        """
        # Only return True to surpress the exception (if any)
        return False 

    def execute(self):
        """
        Executes the command.
        """
        from pymake.util.logger import PymakeLogger

        PymakeLogger.info(self._logname, self._message)
        start = time.clock()
        for i in self._registerables:
            i.register()
        end = time.clock()
        PymakeLogger.info(self._logname, "Register %s items in %s seconds:", len(self._registerables), end - start)
        self._start = time.clock()
