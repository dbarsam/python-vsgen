# -*- coding: utf-8 -*-
"""
This module provides all functionality for the tracking events during an VSG process.

The module defines the class VSGLogger.  The VSGLogger class provides the main functionality of using Python's native logging process.  Since Python allows period-separated hierarchical value (e.g. "VSG.Module.ModuleFeature") and loggers that are further down in the hierarchical list are children of loggers higher up in the list, the VSG Logger manages the hierarchy of loggers in the VSG namespace (i.e. VSG.*).

For completeness, all logging activing in VSG package must go through the VSG Logger.
"""

import os
import sys
import logging


class VSGLogger(object):
    """
    The VSG Logger manages messages associate with various priority level.

    Optional, it can redirect the messages to any output channel (usually a file).
    """

    BASENAME = "VSG"

    class LevelFilter(logging.Filter):
        """
        The LevelFilter class implements a Filter Object specific to the VSGLogger
        """

        def __init__(self, levels=None):
            """
            Constructor
            """
            self._level = levels or [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]

        def filter(self, record):
            """
            Returns NoneZero if the recorsd should be logger; zero otherwise.
            """
            return record.levelno in self._level

    def __init__(self, filepath=None, threshold=logging.INFO):
        """
        Creates a logger with the given name (the name prefixes each log line).

        :param filepath:  The optional output path for the logger messages.
        :param threshold: The threshold for messages; logging messages which are less severe than 'threshold' will be ignored.
        """
        # Create the Logger
        self._logger = self.getLogger(None)
        self._logger.setLevel(threshold)

        # Handler management
        self._fileHandlers = []
        self._handlers = []

        # Register the Standard Output handler
        stdoutHandler = logging.StreamHandler(sys.stdout)
        stdoutHandler.setFormatter(logging.Formatter("%(name)-15s : %(levelname)-8s %(message)s"))
        stdoutHandler.addFilter(VSGLogger.LevelFilter([logging.DEBUG, logging.INFO, logging.WARNING]))
        self._registerHandler(stdoutHandler)

        # Register the Standard Error handler
        stderrHandler = logging.StreamHandler(sys.stderr)
        stderrHandler.setFormatter(logging.Formatter("%(name)-15 : %(levelname)-8s %(message)s"))
        stderrHandler.addFilter(VSGLogger.LevelFilter([logging.ERROR, logging.CRITICAL]))
        self._registerHandler(stderrHandler)

        # Register a File Handler
        if filepath:
            fileHandler = logging.FileHandler(filepath, 'a')
            fileHandler.setFormatter(logging.Formatter("%(asctime)s | %(name)-15 %(levelname)-8s %(message)s", "%b %d %H:%M:%S"))
            self._registerHandler(fileHandler)

    def __del__(self):
        """
        Destructor.
        """
        self.close()

    def _registerHandler(self, handler):
        """
        Registers a handler.

        :param handler:  A handler object.
        """
        self._logger.addHandler(handler)
        self._handlers.append(handler)

    def _unregisterHandler(self, handler, shutdown=True):
        """
        Unregisters the logging handler.

        :param handler:  A handler previously registered with this loggger.
        :param shutdown: Flag to shutdown the handler.
        """
        if handler in self._handlers:
            self._handlers.remove(handler)
            self._logger.removeHandler(handler)
            if shutdown:
                try:
                    handler.close()
                except KeyError:
                    # Depending on the Python version, it's possible for this call
                    # to fail most likely because some logging module objects get
                    # garbage collected before the VSGLogger object is.
                    pass

    @classmethod
    def getLogger(cls, name=None):
        """
        Retrieves the Python native logger

        :param name:    The name of the logger instance in the VSG namespace (VSG.<name>); a None value will use the VSG root.
        :return:        The instacne of the Python logger object.
        """
        return logging.getLogger("{0}.{1}".format(cls.BASENAME, name) if name else cls.BASENAME)

    @classmethod
    def debug(cls, name, message, *args):
        """
        Convenience function to log a message at the DEBUG level.

        :param name:    The name of the logger instance in the VSG namespace (VSG.<name>)
        :param message: A message format string.
        :param args:    The arguments that are are merged into msg using the string formatting operator.
        :..note:        The native logger's `kwargs` are not used in this function.
        """
        cls.getLogger(name).debug(message, *args)

    @classmethod
    def info(cls, name, message, *args):
        """
        Convenience function to log a message at the INFO level.

        :param name:    The name of the logger instance in the VSG namespace (VSG.<name>)
        :param message: A message format string.
        :param args:    The arguments that are are merged into msg using the string formatting operator.
        :..note:        The native logger's `kwargs` are not used in this function.
        """
        cls.getLogger(name).info(message, *args)

    @classmethod
    def warning(cls, name, message, *args):
        """
        Convenience function to log a message at the WARNING level.

        :param name:    The name of the logger instance in the VSG namespace (VSG.<name>)
        :param message: A message format string.
        :param args:    The arguments that are are merged into msg using the string formatting operator.
        :..note:        The native logger's `kwargs` are not used in this function.
        """
        cls.getLogger(name).warning(message, *args)

    @classmethod
    def error(cls, name, message, *args):
        """
        Convenience function to log a message at the ERROR level.

        :param name:    The name of the logger instance in the VSG namespace (VSG.<name>)
        :param message: A message format string.
        :param args:    The arguments that are are merged into msg using the string formatting operator.
        :..note:        The native logger's `kwargs` are not used in this function.
        """
        cls.getLogger(name).error(message, *args)

    @classmethod
    def critical(cls, name, message, *args):
        """
        Convenience function to log a message at the CRITICAL level.

        :param name:    The name of the logger instance in the VSG namespace (VSG.<name>)
        :param message: A message format string.
        :param args:    The arguments that are are merged into msg using the string formatting operator.
        :..note:        The native logger's `kwargs` are not used in this function.
        """
        cls.getLogger(name).critical(message, *args)

    @classmethod
    def exception(cls, name, message, *args):
        """
        Convenience function to log a message at the ERROR level with additonal exception information.

        :param name:    The name of the logger instance in the VSG namespace (VSG.<name>)
        :param message: A message format string.
        :param args:    The arguments that are are merged into msg using the string formatting operator.
        :..note:        This method should only be called from an exception handler.
        """
        cls.getLogger(name).exception(message, *args)

    def close(self):
        """
        Closes and unregisters all logging handlers.
        """
        while self._handlers:
            self._unregisterHandler(self._handlers[0])

if __name__ == "__main__":

    logfile = os.path.join(os.path.dirname(__file__), 'log.txt')
    logger = VSGLogger(logfile, logging.DEBUG)
    VSGLogger.debug("DebugLogger", "Debug = %d", int(logging.DEBUG))
    try:
        raise NotImplementedError("This has not been implemented")
    except:
        VSGLogger.exception(__name__, "Something bad happened.")
    VSGLogger.info(__name__, "This is a multiline logger message:\n %s \n %s \n %s", '****************', 'Message!', '****************')
    VSGLogger.info(__name__, "Info = %d", int(logging.INFO))
    VSGLogger.error("MyName", "Error = %d", int(logging.ERROR))
    VSGLogger.critical("YourName", "Critical = %d", int(logging.CRITICAL))
    VSGLogger.warning(__name__, "Warning = %d", int(logging.WARNING))

    import webbrowser
    webbrowser.open(logfile)
