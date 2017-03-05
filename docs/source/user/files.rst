Configuration Files
===================

vsgen can automatically instantiate and execute any :doc:`objects <objects>` defined in a :mod:`configparser` configuration file.

.. note:: vsgen processes the configuration file with :class:`~configparser.ExtendedInterpolation` available in Python 3's :mod:`configparser`.  There is a  `configparser <https://pypi.python.org/pypi/configparser>`_ Python 2.7 backport of available on the Python Package Index.

Format
------

vsgen uses :class:`~configparser.ConfigParser` to read the configuration files so any file adhering to this standard (a ``setup.cfg`` file, or ``tox.ini``, or a ``vsgen.cfg``) will work.  Sections are introduced by a ``[section]`` header, and contain ``name = value`` entries.  Lines beginning with ``#`` or ``;`` are ignored as comments.

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
VSGen requires a single ``[vsgen]`` section and uses it as an entry point.

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
The absolute path of the ``.sln`` file.

projects
````````
The comma separated list of sections that define projects.

visual_studio_version
`````````````````````
The Visual Studio version number as a float.  E.g ``12.0`` for Visual Studio 2013, ``14.0`` for Visual Studio 2015, etc.  For a full table, consult the enter on `Wikipedia <https://en.wikipedia.org/wiki/Microsoft_Visual_Studio#History>`_.

Project Sections
~~~~~~~~~~~~~~~~
The naming convention for a project section is to follow the ``[vsgen.project.*]`` pattern.

Unlike the solution section a project section can represent one of many projects types.  The project type is controlled by a special ``type`` option and this controls which options are read or ignored in the project section.

The various vales for ``type`` are made available by the respective :doc:`plugins <plugins>` that are available in the current Python session.

Common Options
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
````````
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

Example
-------
The vsgen test suite contains an working example of a configuration file.  The file is available below and at :download:`setup.cfg <..\\..\\..\\tests\\data\\vsgencfg\\setup.cfg>`

.. literalinclude:: ..\..\..\tests\data\vsgencfg\setup.cfg

