Configuration Files
===================

vsgen can automatically instantiate and execute any :doc:`objects` defined in a :mod:`configparser` configuration file.

.. note:: vsgen processes the configuration file with :class:`~configparser.ExtendedInterpolation` available in Python 3's :mod:`configparser`.  There is a  `configparser <https://pypi.python.org/pypi/configparser>`_ Python 2.7 backport of available on the Python Package Index.

Format
------

vsgen uses :class:`~configparser.ConfigParser` to read the configuration files so any fille adherin to this standard (a ``setup.cfg`` file, or ``tox.ini``, or a ``vsgen.cfg``) will work.  Sections are introduced by a ``[section]`` header, and contain ``name = value`` entries.  Lines beginning with ``#`` or ``;`` are ignored as comments.

Main Section
~~~~~~~~~~~~
vsgen will look for a ``[vsgen]`` section and uses it as an entry point.

Object Sections
~~~~~~~~~~~~~~~
vsgen objects are defined in other sections and, out of convention, the sections follow naming pattern ``[vsgen.*]``.



Sections
--------

Main Section
~~~~~~~~~~~~
VSgen requires a single ``[vsgen]`` section and uses it as an entry point.

The following options are options global to the vsgen session.

Options
^^^^^^^
.. contents::
   :local:
   :depth: 2

root
````
A path (relative to the configuration file itself) that is used as a root path.

Solution Sections
~~~~~~~~~~~~~~~~~~
The naming convention for a solution section is the follow the ``[vsgen.solution.*]`` pattern.

Each solution section represents one solution file ``.sln`` and the following options are exposed to define the file.

Options
^^^^^^^
.. contents::
   :local:
   :depth: 2

name
````
The display name of the solution.

filename
````````
The absolute path of the `.sln` file.

projects
````````
The comma separated list of sections that define projects.

visual_studio_version
`````````````````````
The Visual Studio version number as a float.  E.g `12.0` for Visual Studio 2013, `14.0` for Visual Studio 2015, etc.  For a full table, consult the enter on `Wikipedia <https://en.wikipedia.org/wiki/Microsoft_Visual_Studio#History>`_.

Project Sections
~~~~~~~~~~~~~~~~
The naming convention for a project section is to follow the ``[vsgen.project.*]`` pattern.

Unlike the solution section a project section can represent one of many projects types.  The type is controlled by a special ``type`` option this controls which options are read or ignored in the project section.

common options
^^^^^^^^^^^^^^
.. contents::
   :local:
   :depth: 2

name
````
The display name of the project.

type
````
The vsgen project type.  This value describes which project object vsgen will contruct and how the other values in this section are interpreted.

filename
````````````
The absolute path of the ``.proj`` file.

working_directory
`````````````````
The absolute path of the project's working directory.

output_path
```````````
The absolute path of the project's output directory.

root_namespace
``````````````
The fully qualified name space.

project_home 
````````````
The absolute path of the project's home directory.

ptvs options
^^^^^^^^^^^^
A Python Tools for Visual Studio project uses the following extra options.

.. contents::
   :local:
   :depth: 2

search_path
```````````
The comma separated list of absolute paths that define the project's Python search path.

startup_file
````````````
The absolute path of the project's startup file.

compile_files
`````````````
The comma separated list of initial files to be includes as compile files.

content_files
`````````````
The comma separated list of initial files to be includes as content files.
 
compile_in_filter
`````````````````
The comma separated list of file extensions (i.e. .py) used to include files automatically as compile files.

compile_ex_filter
`````````````````
The comma separated list of file extensions (i.e. .py) used to exclude files automatically from compile files.

content_in_filter
`````````````````
The comma separated list of file extensions (i.e. .py) used to include files automatically as content files.

content_ex_filter
`````````````````
The comma separated list of file extensions (i.e. .py) used to exclude files automatically from content files.

directory_in_filter
```````````````````
The comma separated list of path glob patterns used to include directories when autoamtically adding files.

directory_ex_filter
```````````````````
The comma separated list of path glob patterns used to exclude directories when autoamtically adding files.

is_windows_application
``````````````````````
Flag denoting if we're using python.exe or pythonw.exe as a launcher.

python_interpreter
``````````````````
The section defining the selected Python interpreters of this project.

python_interpreter_args
```````````````````````
The comman separated list of python interpreter arguments.

python_interpreters
```````````````````
The comma separated list of sections that define Python interpreters used by this project.

python_virtual_environments
```````````````````````````
The comma separated list of sections that define Python virtual environments used by this project.

Interpreter Section
~~~~~~~~~~~~~~~~~~~~~~~~~~
A Python Tools for Visual Studio project uses one of more Python Interpreters.  Each interpretter could by a stanrad Python installation or a Pytyon virtual environment; however all interpreters are managed outside of Visual Studio and the projects include them as section references.

If the interpreter is a standard python interpreter the naming convention is ``[pyvsgen.interpreter.*]``.

If the interpreter is a virtual environment the naming convention is ``[vsgen.virtual_environment.*]``.

.. contents::
   :local:
   :depth: 2

Interpreter Options
^^^^^^^^^^^^^^^^^^^
A Python Tools for Visual Studio interpreter uses the following extra options.

interpreter_paths
`````````````````
The comma separated list of absolute paths that contain python installations.

description
```````````
The display description of the environment.

Virtual Environment options
^^^^^^^^^^^^^^^^^^^^^^^^^^^
A Python Tools for Visual Studio virtual environment uses the following extra options.

environment_paths
`````````````````
The comma separated list of absolute paths that contain virtual environments.

description
```````````
The display description of the interpreter.

Example
-------
The vsgen test suite contains an working example of a configuration file.  The file is available below and at :download:`setup.cfg <..\\..\\..\\tests\\data\\vsgencfg\\setup.cfg>`

.. literalinclude:: ..\..\..\tests\data\vsgencfg\setup.cfg

