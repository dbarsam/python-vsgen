===============
Release Process
===============

This process describes the steps to execute the automated release workflow for `vsgen`.  This workflow consists of:

#. A new release being generated on GitHub.
#. The release built and validated by `AppVeyor`_.
#. The documentation updated on the `Read the Docs`_.
#. The Python package updated on `PyPI`_.

Prerequisites
=============

#. Close all `tickets for the next version`_.

#. Update the *minimum* version of all requirements in :file:`setup.py`.

#. Update the *exact* version of all requirements in :file:`requirements.txt`.

#. Run :command:`python setup.py test` from the project root. All tests for all supported
   versions must pass:

   .. code-block:: bat

    $ python setup.py test
    [...]
    ________ summary ________
    OK    

#. Run :command:`python setup.py pep8` from the project root.  All pep8 
   validations must pass:

   .. code-block:: bat

    $ python setup.py pep8
    running pep8

#. Build the docs.  While the final target is HTML there are additional steps to execute.  Make sure there are no errors and undefined
   references.

   .. code-block:: bat

    $ cd docs/
    $ pip install -r requirements.txt
    $ make.bat clean 
    $ make.bat rst
    $ make.bat html
    $ make.bat view
    $ cd ..

#. Update the change log :file:`CHANGES.txt` by reviewing the changes since last release on the `github compare`_ site or from the command line:

   .. code-block:: bat

	$ for /f "delims=" %a in ('git describe --tags --abbrev^=0') do @git log %a..HEAD --oneline --decorate

#. Commit all changes:

   .. code-block:: bat

    $ git commit -m 'Updated change log for upcoming release.'

Build
=====

#. Build a source distribution and a `wheel`_ package and test them:

   .. code-block:: bat

    $ python setup.py sdist bdist_wheel
    $ ls dist/
    vsgen-a.b.c-py2.py3-none-any.whl vsgen-a.b.c.tar.gz

#. Install the source distribution:

   Ensure clean state if ran repeatedly:

   .. code-block:: bat

    $ rm -rf %TEMP%\vsgen-sdist

   Create a virtual environment and install the distribution:

   .. code-block:: bat

    $ virtualenv %TEMP%\vsgen-sdist
    $ %TEMP%\vsgen-sdist\activate
    (vsgen-sdist) $ pip install .\dist\vsgen-a.b.c.zip
    (vsgen-sdist) $ python
    >>> import vsgen
    >>> vsgen.__version__
    'a.b.c'

#. Instal the wheel distribution:

   Ensure clean state if ran repeatedly:

   .. code-block:: bat

    $ rm -rf %TEMP%\vsgen-wheel

   Create a virtual environment and install the distribution:

   .. code-block:: bat

    $ virtualenv %TEMP%\vsgen-wheel
    $ %TEMP%\vsgen-wheel\activate
    (vsgen-wheel) $ pip install .\dist\vsgen-a.b.c-py2.py3-none-any.whl
    (vsgen-wheel) $ python
    >>> import vsgen
    >>> vsgen.__version__
    'a.b.c'

Release
=======

#. Sync the local branch with the remote master branch and verify that the `Appveyor`_ dashboard is passing.

#. Navigate to vsgen's `release page`_ and draft a new release:
   
   #. Give the release a title (`Feature Release`, `Maintenance Release`, etc.).
   #. Tag with the appropriate version as described in :file:`CHANGES.txt`.

#. Publish the release:
   
   #. Verify that the `Appveyor`_ dashboard is green and has published the package to `PyPI`_.
   #. Verify that the `Read the Docs`_ is updated.

#. Check if the package is displayed correctly: https://pypi.python.org/pypi/vsgen

Post release
============

Finally instal vsgen one last time:

   Ensure clean state if ran repeatedly:

   .. code-block:: bat

    $ rm -rf %TEMP%\vsgen-pip

   Create a virtual environment and install the distribution:
   
   .. code-block:: bat
   
    $ virtualenv %TEMP%\vsgen-pip
    $ %TEMP%\vsgen-pip\activate
    (vsgen-pip) $ pip install -U vsgen
    (vsgen-pip) $ python
    >>> import vsgen
    >>> vsgen.__version__
    'a.b.c'

.. _pypi: https://pypi.python.org/pypi
.. _wheel: https://pypi.python.org/pypi/wheel
.. _read the docs: http://vsgen.readthedocs.org/en/latest/
.. _appveyor: https://ci.appveyor.com/project/DBarsam/python-vsgen
.. _release page: https://github.com/dbarsam/python-vsgen/releases
.. _tickets for the next version: https://github.com/dbarsam/python-vsgen/issues?q=is%3Aopen+is%3Aissue
.. _github compare: https://github.com/dbarsam/python-vsgen/compare