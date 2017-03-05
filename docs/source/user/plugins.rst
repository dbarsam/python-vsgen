Plugins
=======
A vsgen plugin defines additional :doc:`objects <objects>` that can be instantiated by vsgen during normal operations.

Entry Points
------------
An entry point is a `setuptools' <http://setuptools.readthedocs.io/en/latest/setuptools.html>`_ packaging mechanism that makes Python objects discoverable to other packages.  

The syntax of the entry point has various components and vsgen uses multiple context groups to organise the various objects a plugin can define.  Each group is prefixed with the ``vsgen`` name and follows the following model::

    'vsgen.<group>': [
        '<key> = <module>:<class>'
    ],

group
    The object class.  One of ``Projects`` or ``Suites``.

key
	The public identifier of the object within the context group.

module
	The module import path containing the object.

class
	The object name within the module. 

A Python package can define multiple entry points, however, vsgen expect the ``key`` value to be unique within the Python session.  If different Python packages register classes under the same key one will override the other.

Plugin Example: *ExamplePlugin*
-------------------------------

An Exmaple plugin ``EP`` exposes two entrypoints in its ``setup.py`` file::

    'vsgen.suites': [
        'ep = vsgenep.suite:EPSuite'
    ],
    'vsgen.projects': [
        'ep = vsgenep.project:EPProject'
    ]

The first registers the ``EPSuite`` class in the ``vsgenep.suite`` module with the ``ep`` key.  The entry point makes the ``EPSuite`` discoverable by vsgen when it queries the current Python environment for all :class:`vsgen.suite.VSGSuite` implementing classes.

The second registers the ``EPProject`` class in the ``vsgenep.project`` module with the ``ep`` key.  The entry point makes the ``EPProject`` discoverable by vsgen when it queries the current Python environment for all :class:`vsgen.project.VSGProject` implementing classes.