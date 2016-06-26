===============
Release Process
===============

This process describes the steps to execute the automated release workflow for `vsgen`.  This workflow consists of:

#. A new release being generated on GitHub.
#. The release built and validated by `AppVeyor <https://ci.appveyor.com/project/DBarsam/python-vsgen>`_.
#. The documentation updated on the `Read the Docs <http://vsgen.readthedocs.org/en/latest/>`_.
#. The Python package updated on `PyPI <https://pypi.python.org/pypi/vsgen>`_.

Prerequisites
=============

#. Close all `tickets for the next version
   <https://github.com/dbarsam/python-vsgen/issues?q=is%3Aopen+is%3Aissue>`_.

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

#. Build the docs (HTML is enough). Make sure there are no errors and undefined
   references.

   .. code-block:: bat

    $ cd docs/
    $ make.bat clean 
    $ make.bat html
    $ make.bat view
    $ cd ..

#. Update the change log (:file:`CHANGES.txt`).

#. Commit all changes:

   .. code-block:: bat

	$ git commit -m 'Updated change log for upcoming release.'

Build
=====

#. Build a source distribution and a `wheel <https://pypi.python.org/pypi/wheel>`_
   package and test them:

   .. code-block:: bat

    $ python setup.py sdist bdist_wheel
    $ ls dist/
    vsgen-a.b.c-py2.py3-none-any.whl vsgen-a.b.c.tar.gz

#. Install the source distribution:

   .. code-block:: bat

    $ rm -rf %TEMP%\vsgen-sdist  # ensure clean state if ran repeatedly
    $ virtualenv %TEMP%\vsgen-sdist
    $ %TEMP%\vsgen-sdist\activate
    (vsgen-sdist) $ pip install .\dist\vsgen-a.b.c.zip
    (vsgen-sdist) $ python
    >>> import vsgen
    >>> vsgen.__version__
    'a.b.c'

#. Installing the wheel distribution:

   .. code-block:: bat

    $ rm -rf %TEMP%\vsgen-wheel  # ensure clean state if ran repeatedly
    $ virtualenv %TEMP%\vsgen-wheel
    $ %TEMP%\vsgen-wheel\activate
    (vsgen-wheel) $ pip install .\dist\vsgen-a.b.c-py2.py3-none-any.whl
    (vsgen-wheel) $ python
    >>> import vsgen
    >>> vsgen.__version__
    'a.b.c'

Release
=======

#. Sync the local branch with the remote master branch and verify that
   the `Appveyor dashbaord <https://ci.appveyor.com/project/dbarsam/python-vsgen>`_ is passing.

#. Navigate to vsgen's `Release Page <https://github.com/dbarsam/python-vsgen/releases>`_
   and draft a new release:
   
   #. Give the release a title (`Feature Release`, `Maintenance Release`, etc.).
   #. Tag with the appropriate version as described in :file:`CHANGES.txt`.

#. Publish the release:
   
   #. Verify that the `Appveyor dashboard <https://ci.appveyor.com/project/DBarsam/python-vsgen>`_
      is green and has published the package to `PyPI <https://pypi.python.org/pypi>`_.
   #. Verify that the `Read the Docs <http://vsgen.readthedocs.io/en/latest/>`_
      is updated.

#. Check if the package is displayed correctly:
   https://pypi.python.org/pypi/vsgen

Post release
============

Finally instal vsgen one last time:

   .. code-block:: bat

    $ rm -rf %TEMP%\vsgen-pip  # ensure clean state if ran repeatedly
    $ virtualenv %TEMP%\vsgen-pip
    $ %TEMP%\vsgen-pip\activate
    (vsgen-pip) $ pip install -U vsgen
    (vsgen-pip) $ python
    >>> import vsgen
    >>> vsgen.__version__
    'a.b.c'
