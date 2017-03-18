Introduction
============
VSGen is a framework to generate Microsoft Visual Studio Solutions and Projects from Python script or configuration files.

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

Quick Start
-----------
VSGen is the entry point however the data needed to generate specific projects (CPP, C#, Python,e tc.) are availabel in VSGen plugins.

To see which plugins are installed:: 

    vsgen auto --help

To automatically create a solution and project from the command line, use the ``auto`` command::

	vsgen auto <type> <path> <type options>

For example, to create a PTVS solution and project (using the `vsgen-ptvs <https://pypi.python.org/pypi/vsgen-ptvs>`_ Python package) pointing at ``S:\project`` and named ``demo``::

	vsgen auto ptvs --root S:\project --name demo

Usage
-----
There are two ways to use vsgen:

#. Creating objects explicitly using Python code and invoking the desired functions from within a Python session.
#. Defining objects using one or more configuration file and processing it with vsgen on the command line.
    
Using Python Code
~~~~~~~~~~~~~~~~~
The functionality of vsgen is organised into classes and can be manipulated by Python code.  More information is available on the :doc:`objects` page.

Command Line
~~~~~~~~~~~~

Using Configuration Files
*************************
Vsgen supports reading in solution and project defintions defined in :mod:`configparser` configuration files.  More information is available on the :doc:`files` page.

.. note:: vsgen processes the configuration file with :class:`~configparser.ExtendedInterpolation` available in Python 3's :mod:`configparser`.  There is a  `configparser <https://pypi.python.org/pypi/configparser>`_ Python 2.7 backport of available on the Python Package Index.

Automatic Generation
********************
Vsgen supports automatic generation given a directory and a type.  The type corresponds to any Vsgen plugins that has been installed.

Execution
---------
Vsgen has a simple command line interface.

You can run it as a module::

	$ python -m vsgen ...
    
or, when installed with setuptools, run the auto generated entry point in Scripts::

	$ vsgen ...

Command Line Reference
~~~~~~~~~~~~~~~~~~~~~~
The complete command line interface is below:

.. argparse::
    :ref: vsgen.__main__.make_documentation_parser
    :prog: vsgen
	:nodefault:

Getting help
------------

Check out the :doc:`FAQ <faq>` or submit a bug report to the `Github issue tracker <https://github.com/dbarsam/python-vsgen/issues>`_.
