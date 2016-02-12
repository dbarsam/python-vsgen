Introduction
===============

VSGen generates Microsoft Visual Studio Solutions and Projects from Python script or configuration files.

.. note:: Currently only `Python Tools for Visual Studio <https://github.com/Microsoft/PTVS>`_ projects are supported.

Install
-------
The package is designed to work with pip.

To install the package::

   pip install vsgen

To uninstall the package::

   pip uninstall vsgen

To upgrade the package::

   pip install --upgrade vsgen
   
Starting with Python 2.7.9, pip is included by default with the Python binary installers.

Usage
-----
There are two ways to use vsgen:

#. Creating objects explicitly using Python code and invoking the desired functions from within a Python session.
#. Defining objects using one or more configuration file and processing it with vsgen on the command line.
    
Using Python Code
~~~~~~~~~~~~~~~~~
The functionality of vsgen is organised into classes and can be manipulated by Python code.  More information is available on the :doc:`objects` page.

Using Configuration Files
~~~~~~~~~~~~~~~~~~~~~~~~~
Vsgen also supports reading in solution and project defintions defined in :mod:`configparser` configuration files.  More information is available on the :doc:`files` page.

.. note:: vsgen processes the configuration file with :class:`~configparser.ExtendedInterpolation` available in Python 3's :mod:`configparser`.  There is a  `configparser <https://pypi.python.org/pypi/configparser>`_ Python 2.7 backport of available on the Python Package Index.

Command line options
~~~~~~~~~~~~~~~~~~~~
vsgen has a simple command line interface and allows specifiying one or more :doc:`configuration files <files>`.

You can run it as a module::

	python -m vsgen [-h] file [file ...]
    
or when install with setuptools run the auto generated entry point in Scripts::

	vsgen [-h] file [file ...]

A quick help is available on the command line::

    $ python vsgen -h
    usage: vsgen [-h] file [file ...]

    Executes the vsgen package as an application.

    positional arguments:
      file        The configuration file that contains the [vsgen.*] sections
                  contains the vsgen input

    optional arguments:
      -h, --help  show this help message and exit

Getting help
------------

Check out the :doc:`FAQ <faq>` or submit a bug report to the `Github issue tracker <https://github.com/dbarsam/python-vsgen/issues>`_.
