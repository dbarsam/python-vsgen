Classes
=======
vsgen provides a collection of Python classes that represent solutions, projects, and other concepts used by Visual Studio to organise resources.

.. seealso:: Microsoft's `Solutions and Projects in Visual Studio <https://msdn.microsoft.com/en-us/library/b142f8e7.aspx>`_

Interfaces
----------
Each object executes one or more `actions` and vsgen uses a small collection of interface to define the actions.

The `Writable` Interface
~~~~~~~~~~~~~~~~~~~~~~~~
The :class:`~vsgen.writer.VSGWritable` implements a base class for all objects that `writes` as it's action.

The `Registerable` Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The :class:`~vsgen.register.VSGRegisterable` is the base class for all objects that `registers` as its action.

Commands
--------
For efficiency and conveneinve vsgen provides `command` objects that adapt each interface object into an efficient execution model.

The `Write` Command
~~~~~~~~~~~~~~~~~~~
The :class:`~vsgen.writer.VSGWritCommand` is the command to efficient execute any :class:`~vsgen.writer.VSGWritable` action.

The `Register` Command
~~~~~~~~~~~~~~~~~~~~~~
The :class:`~vsgen.register.VSGRegisterCommand` is the command to efficient execute any :class:`~vsgen.writer.VSGRegisterable` action.

Solutions
---------
Visual Studio currently uses one solution type so vsgen currently provides a single solution, the :class:`~vsgen.solution.VSGSolution` class.

The :class:`~vsgen.solution.VSGSolution` is designed to represent a single ``.sln`` solution file; it contains basic attributes (:attr:`~vsgen.solution.VSGSolution.Name` and :attr:`~vsgen.solution.VSGSolution.FileName`) and a collection of :attr:`~vsgen.solution.VSGSolution.Projects`, represented by :class:`~vsgen.solution.VSGProject` dervied classes.

The implements the :class:`~vsgen.writer.VSGWritable` interface.

Projects
--------
Visual Studio handles different project types so vsgen currently provides a base project class :class:`~vsgen.project.VSGProject` for other classes to inheriut and specialize.  It contains only basic attributes such as :attr:`~vsgen.project.VSGProject.Name`, :attr:`~vsgen.project.VSGProject.FileName`, etc.

.. note:: vsgen only provides support for one project, the Python Tools for Visual Studio The :class:`~vsgen.ptvs.project.PTVSProject` class.

Python Tools for Visual Studio Projects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The Python Tools for Visual Studo projects extends the base :class:`~vsgen.project.VSGProject` with the :class:`~vsgen.ptvs.project.PTVSProject` class.

Other Classes
-------------

Python Tools for Visual Studio Interpreters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Python Tools for Visual Studio projects require a Python environment (or Python virtual environment) to exist on the user's machine and be `manually registered <https://github.com/Microsoft/PTVS/wiki/Python-Environments>`_ with Visual Studio.  To automate this each Python environment is represented by a :class:`~vsgen.ptvs.interpreter.PTVSInterpreter` class.

.. note:: The :class:`~vsgen.ptvs.interpreter.PTVSInterpreter` does not create or install a Python interpreter.  Instead it stores the Visual Studio specific definition of that environment and resolves the information for the project.  If the environment does not exist vsgen will throw an exception.

Python Tools for Visual Studio uses a Windows registry key to store Python environment information.  When vsgen process an interpret object, it will do one of two things:

#. Create the respective Windows registry key.
#. Match the environment information against and existing Windows registry key.

In both cases however, the project is guarateed it's environment will be recognised by Visual Studio.


Example
-------
The vsgen test suite contains an working example of using the objects in a demo package:

.. literalinclude:: ..\..\..\tests\data\vsgendemo\__main__.py
