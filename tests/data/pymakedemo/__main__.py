# -*- coding: utf-8 -*-
"""
Generates the Pymake Demo's Python Tools for Visual Studio IDE Solutions and Projects.  
"""
import os
import sys

def main(argv=[]):
    """
    The entry point of the script.

    It will generate the Python Tools for Visual Studio IDE Solutions and Project as per configured.
    """
    from pymake import PyWriteCommand, PyRegisterCommand, PymakeLogger
    from pymakedemo.solutions import PymakeDemoSolution

    # logger
    pylogger = PymakeLogger()

    # Solutions
    solutions = [PymakeDemoSolution()]
    with PyWriteCommand('PymakeDemo', solutions) as command:
        command.execute()

    # Projects
    projects = set(sorted((p for s in solutions for p in s.Projects), key=lambda x: x.Name))
    with PyWriteCommand('PymakeDemo', projects) as command:
        command.execute()

    # Interpretters
    interpretters = set(i for p in projects for i in p.PythonInterpreters)
    with PyRegisterCommand('PymakeDemo', interpretters) as command:
        command.execute()

    return 0

if __name__ == "__main__":
    # To use PymakeDemo as a package we need to append the sys.path before executing main
    filePath = os.path.dirname( os.path.realpath(__file__) )
    for path in [os.path.normpath(p) for p in [os.path.join( filePath, '..'), os.path.join( filePath, '..', '..', '..')] if p not in sys.path]:
        sys.path.append(path)

    sys.exit(main(sys.argv))
