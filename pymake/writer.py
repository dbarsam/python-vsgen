# -*- coding: utf-8 -*-
"""
This module provides a simple multi-threaded writer utility for PymakeProjects and PymakeSolutions
"""

import time
import threading

class PyWritable(object):
    """
    An interface class defining methods necessary for PymakeWriter
    """
    __writable_name__ = "Unknown Writable"

    def write( self ):
        raise NotImplementedError( "Should have implemented this" )

class PyWriteCommand(object):
    """
    The PyWriteCommand class presents a simple command object to execute the writing methods of a collection of PyWritable objects.
    """
    def __init__(self, logname, writables):
        """
        Initializes the instance with an default values.

        @param message:  The display message when using the time in a context manager (e.g the __enter__/__exit__ methods).
        """
        self._logname = logname
        self._writables = writables
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
        from pymake.util.logger import PymakeLogger

        PymakeLogger.info(self._logname, self._message)
        start = time.clock()
        PymakeWriter.write(self._writables)
        end = time.clock()
        PymakeLogger.info(self._logname, "Wrote %s files in %s seconds:", len(self._writables), end - start)


class PymakeWriter(threading.Thread):
    """
    PymakeWriter encapsulates the logic needed to write any Pymake object to disk.
    """
    def __init__(self, pylist):
        """
        PymakeProject encapsulates the logic needed to create a *.pyproject file.

        :param pylist: A list of Pymake objects[PrProjects, PymakeSolutions, etc]
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
        Utility method to spawn a PymakeWriter for each element in a collection.

        :param pylist:   A list of Pymake objects (PrProjects, PymakeSolutions, etc)
        :param parallel: Flag to execute the process in parallel (i.e. use python threads).
        """
        threads = [PymakeWriter(o) for o in pylist]
        if parallel:
            for t in threads:
                t.start()
            for t in threads:
                t.join()
        else:
            for t in threads:
                t.run()
