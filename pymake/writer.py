# -*- coding: utf-8 -*-
"""
This module provides a simple multi-threaded writer utility for PymakeProjects and PymakeSolutions
"""

import threading

class PyWritable(object):
    """
    An interface class defining methods necessary for PymakeWriter
    """
    def write( self ):
        raise NotImplementedError( "Should have implemented this" )

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
