# -*- coding: utf-8 -*-
"""
This module provides all functionality for the timing actions during an VSG process.

The module defines the class VSGTimer.  The VSGTimer is a simple timer to time processes.
"""

import time

from vsgen.util.logger import VSGLogger


class VSGTimer(object):
    """
    The VSGTimer class presents a simply timer using Python's native time module.
    """

    def __init__(self, message=None):
        """
        Initializes the instance with an default values.

        :param message:  The display message when using the time in a context manager (e.g the __enter__/__exit__ methods).
        """
        self._message = message
        self._start = 0
        self._stop = 0

    def __enter__(self):
        """
        Convenience method to be used with Python's 'with' function.  Starts the timer.

        Example:

            with VSGTimer("message") as simple_timer:
                ...

        """
        self.start(self._message)
        return self

    def __exit__(self, type, value, tb):
        """
        Convenience method to be used with Python's 'with' function.  Stops the timer initiated with the __enter__ method.
        """
        self.stop(self._message)

    def start(self, message):
        """
        Manually starts timer with the message.

        :param message:  The display message.
        """
        self._start = time.clock()
        VSGLogger.info("{0:<20} - Started".format(message))

    def stop(self, message):
        """
        Manually stops timer with the message.

        :param message:  The display message.
        """
        self._stop = time.clock()
        VSGLogger.info("{0:<20} - Finished [{1}s]".format(message, self.pprint(self._stop - self._start)))

    def pprint(self, seconds):
        """
        Pretty Prints seconds as Hours:Minutes:Seconds.MilliSeconds

        :param seconds:  The time in seconds.
        """
        return ("%d:%02d:%02d.%03d", reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(seconds * 1000,), 1000, 60, 60]))
