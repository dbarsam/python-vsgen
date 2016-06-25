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

Command Line
~~~~~~~~~~~~

Using Configuration Files
*************************
Vsgen supports reading in solution and project defintions defined in :mod:`configparser` configuration files.  More information is available on the :doc:`files` page.

.. note:: vsgen processes the configuration file with :class:`~configparser.ExtendedInterpolation` available in Python 3's :mod:`configparser`.  There is a  `configparser <https://pypi.python.org/pypi/configparser>`_ Python 2.7 backport of available on the Python Package Index.

Automatic Generation
********************
Vsgen supports automatic generation given a directory and a type.  The type corresponds to a template file in vsgen's ``data`` directory.

Command line options
~~~~~~~~~~~~~~~~~~~~
vsgen has a simple command line interface and allows specifiying one or more :doc:`configuration files <files>`.

You can run it as a module::

	$ python -m vsgen [-h] {generate,auto} ...
    
or when install with setuptools run the auto generated entry point in Scripts::

	$ vsgen [-h] {generate,auto} ...

A quick help is available on the command line::

	$ python vsgen --help                                                          
	usage: vsgen [-h] {generate,auto} ...                                          
                                                                               
	Executes the VSG package as an application.                                    
                                                                               
	positional arguments:                                                          
	  {generate,auto}  Available commands.                                         
		generate       Generates solutions and projects based on one or more       
					   configuration files.                                        
		auto           Automatically generates a solution and project from a       
					   single directory.                                           
                                                                               
	optional arguments:                                                            
	  -h, --help       show this help message and exit                             
                                                                               

Getting help
------------

Check out the :doc:`FAQ <faq>` or submit a bug report to the `Github issue tracker <https://github.com/dbarsam/python-vsgen/issues>`_.
