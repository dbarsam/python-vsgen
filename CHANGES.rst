Changelog
=========

1.0.0-dev_ (Unreleased)
-----------------------
- TBD

0.3.0_ (2017-03-18) 
-------------------
Features:

- Modularize VSGen with setuptool's entry points; Fixes #11.

Compatibility Notes:

- A plugin architecture has been adopted starting with 0.3.0_.  The vsgen package is now a **core** module and any metadata and code used to generates specific projects should be placed in a **plugin** module.
- The former Python Tools for Visual Studio functionality that was embedded in vsgen has been extracted to `vsgen-ptvs <https://pypi.python.org/pypi/vsgen-ptvs>`_

0.2.4_ (2017-02-18) 
-------------------
Features:

- Refactored the command line argument structure to expose more options to the command line; Fixes #10.
- Adopted fnmatch_ pattern style for file and directory filter patterns, e.g ``.txt`` is now ``*.txt``.

Bug Fixes:

- Fixed auto command's resolution of the current directory; Fixes #9.

0.2.3_ (2016-06-24) 
-------------------
Features:

- Added automatic project generation; Fixes #6.

0.2.2_ (2016-05-29) 
-------------------
Bug Fixes:

- Fixed mishandling of mkdir command; Fixes #4.

0.2.1_ (2016-03-09) 
-------------------
Bug Fixes:

- Updated main's argument handling; Fixes #1.
- Added missing import; Fixes #2.
- Fixed misnamed PTVSInterpreter class variable; Fixes #3.

0.2.0, 2016-03-08
------------------
- Initial Release.

.. _0.3.0: https://github.com/dbarsam/python-vsgen/compare/0.2.4...0.3.0
.. _0.2.4: https://github.com/dbarsam/python-vsgen/compare/0.2.3...0.2.4
.. _0.2.3: https://github.com/dbarsam/python-vsgen/compare/0.2.2...0.2.3
.. _0.2.2: https://github.com/dbarsam/python-vsgen/compare/0.2.1...0.2.2
.. _0.2.1: https://github.com/dbarsam/python-vsgen/compare/0.2.0...0.2.1
.. _1.0.0-dev: https://github.com/dbarsam/python-vsgen/compare/0.3.0...HEAD
.. _fnmatch: https://docs.python.org/2/library/fnmatch.html
