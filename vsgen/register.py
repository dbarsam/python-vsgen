# -*- coding: utf-8 -*-
"""
This module provides a simple register utility for VSGenerate objects.
"""
import sys
import time


class VSGRegisterable(object):
    """
    An interface class defining methods necessary for VSGRegisterable
    """
    __resgisterable_name__ = "Unknown Resgisterable"

    def register(self):
        """
        Interface method to 'register' the object.
        """
        raise NotImplementedError("Should have implemented this")

    def text(self, value):
        """
        Converts a value to text in a way compatible with Python2 and Python 3.

        :param object value:  The value to convert.
        :return:  The value as text.
        """
        return unicode(value) if sys.version_info < (3,) else str(value)

    def upper(self, value):
        """
        Converts a value to upper case text in a way compatible with Python2 and Python 3.

        :param object value:  The value to convert.
        :return:  The value as upper case text.
        """
        return self.text(value).upper()

    def lower(self, value):
        """
        Converts a value to lower case in a way compatible with Python2 and Python 3.

        :param object value:  The value to convert.
        :return:  The value as lower case text.
        """
        return self.text(value).lower()


class VSGRegisterCommand(object):
    """
    The VSGRegisterCommand class presents a simple command object to execute the register methods of a collection of VSGRegisterable objects.
    """

    def __init__(self, logname, registerables):
        """
        Initializes the instance with an collection of registerables.

        :param str logname:  The python logger log name.
        :param list registerables:  The list of VSGRegisterable class instances.
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
        from vsgen.util.logger import VSGLogger

        VSGLogger.info(self._logname, self._message)
        start = time.clock()
        for i in self._registerables:
            i.register()
        end = time.clock()
        VSGLogger.info(self._logname, "Register %s items in %s seconds:", len(self._registerables), end - start)
        self._start = time.clock()
