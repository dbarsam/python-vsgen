Classes
=======
vsgen provides a collection of Python classes that represent solutions, projects, and other concepts used by Visual Studio to organise resources.

.. seealso:: Microsoft's `Solutions and Projects in Visual Studio <https://msdn.microsoft.com/en-us/library/b142f8e7.aspx>`_

Interfaces
----------
Each vsgen object executes one or more *actions* and vsgen uses a small collection of interface to define these actions.

The *Writable* Interface
~~~~~~~~~~~~~~~~~~~~~~~~
The :class:`~vsgen.writer.VSGWritable` is a base class for all objects that *writes* to the disk.

The *Registerable* Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The :class:`~vsgen.register.VSGRegisterable` is the base class for all objects that *registers* data with operating system.

Commands
--------
For efficiency and conveneinve vsgen provides *command* objects that adapt each interface object into an vsgen's execution model.

The *Write* Command
~~~~~~~~~~~~~~~~~~~
The :class:`~vsgen.writer.VSGWriteCommand` is the command object that executes any :class:`~vsgen.writer.VSGWritable` implementing object.

The *Register* Command
~~~~~~~~~~~~~~~~~~~~~~
The :class:`~vsgen.register.VSGRegisterCommand` is the command object that executes any :class:`~vsgen.writer.VSGRegisterable` implementing object.

Solutions
---------
Visual Studio currently uses one solution type so vsgen currently provides a single solution, the :class:`~vsgen.solution.VSGSolution` class.

The :class:`~vsgen.solution.VSGSolution` is designed to represent a single ``.sln`` solution file; it contains basic attributes (:attr:`~vsgen.solution.VSGSolution.Name` and :attr:`~vsgen.solution.VSGSolution.FileName`) and a collection of :attr:`~vsgen.solution.VSGSolution.Projects` that contains a number of :class:`~vsgen.solution.VSGProject` dervied classes.

The solution class implements the :class:`~vsgen.writer.VSGWritable` interface.

Projects
--------
Visual Studio handles different project types so vsgen currently provides a base project class :class:`~vsgen.project.VSGProject` for other classes to inherit and specialize.

Since it is a base class, it contains only basic attributes such as :attr:`~vsgen.project.VSGProject.Name`, :attr:`~vsgen.project.VSGProject.FileName`, etc.  Plugins will inherit from :class:`~vsgen.project.VSGProject` and extended it with additional attributes and methods needed to define their respective Visual Studio projects.

Suites
------
Suites are user defined groupings of solutions and projects.  These groups are repsent the pre-set configuration and are invoked by the ``auto`` command.  VSGen provides a base :class:`~vsgen.suite.VSGSuite` for other classes to inherit and extend.

Example
-------
The vsgen test suite contains an working example of using the objects in a demo package:

.. literalinclude:: ..\..\..\tests\data\vsgendemo\__main__.py
