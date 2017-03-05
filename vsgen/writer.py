# -*- coding: utf-8 -*-
"""
This module provides a simple multi-threaded writer utility for VSGProjects and VSGSolutions
"""
import sys
import time
import threading


class VSGWritable(object):
    """
    An interface class defining methods necessary for VSGWriter
    """
    __writable_name__ = "Unknown Writable"

    def write(self):
        """
        Interface method to 'write' the object.
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


class VSGWriteCommand(object):
    """
    The VSGWriteCommand class presents a simple command object to execute the writing methods of a collection of VSGWritable objects.
    """

    def __init__(self, logname, writables, parallel=True):
        """
        Initializes the instance with an default values.

        :param str logname:  The python logger log name.
        :param list writables:  The list of VSGWritable class instances.
        :param bool parallel: Flag to enable asynchronous writing.
        """
        self._logname = logname
        self._writables = writables
        self._parallel = parallel
        writables_names = set([w.__writable_name__ for w in writables])
        if not writables_names:
            self._message = "Writing no files."
        elif len(writables_names) == 1:
            self._message = "Writing {0}{1}".format(next(iter(writables_names)), 's' if len(writables) > 1 else '')
        else:
            self._message = "Writing a mixed collection of files."

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
        VSGWriter.write(self._writables, self._parallel)
        end = time.clock()
        VSGLogger.info(self._logname, "Wrote %s files in %s seconds:", len(self._writables), end - start)


class VSGWriter(threading.Thread):
    """
    VSGWriter encapsulates the logic needed to write any VSG object to disk.
    """

    def __init__(self, pylist):
        """
        VSGProject encapsulates the logic needed to create a *.pyproject file.

        :param list pylist: A list of VSG objects[PrProjects, VSGSolutions, etc]
        """
        threading.Thread.__init__(self)
        if not hasattr(pylist, '__iter__'):
            self._pylist = [pylist]
        else:
            self._pylist = pylist

    def run(self):
        """
        The Thread's execution function.
        """
        for pyitem in self._pylist:
            pyitem.write()

    @staticmethod
    def write(pylist, parallel=True):
        """
        Utility method to spawn a VSGWriter for each element in a collection.

        :param list pylist:   A list of VSG objects (PrProjects, VSGSolutions, etc)
        :param bool parallel: Flag to enable asynchronous writing.
        """
        threads = [VSGWriter(o) for o in pylist]
        if parallel:
            for t in threads:
                t.start()
            for t in threads:
                t.join()
        else:
            for t in threads:
                t.run()
