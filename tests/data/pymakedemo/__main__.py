# -*- coding: utf-8 -*-
"""
Generates the Pymake Demo's Python Tools for Visual Studio IDE Solutions and Projects.  
"""
import os
import sys
import time

def main(argv=[]):
    """
    The entry point of the script.

    It will generate the Python Tools for Visual Studio IDE Solutions and Project as per configured.
    """
    from pymake import PymakeWriter, PymakeLogger
    from pymakedemo.settings import PymakeDemoSettings
    from pymakedemo.solutions import PymakeDemoSolution

    # logger
    pylogger = PymakeLogger()

    # Solutions
    solutions = [PymakeDemoSolution()]
    
    # Solutions
    solutions = sorted(solutions)
    pylogger.info("PymakeDemo", "Writing Pymake Solutions")
    start = time.clock()
    PymakeWriter.write(solutions)
    end = time.clock()
    pylogger.info("PymakeDemo", "Wrote {0} solution files in {1} seconds:".format(len(solutions), end - start))

    # Projects
    projects = set(sorted((p for s in solutions for p in s.Projects), key=lambda x: x.Name))
    pylogger.info("PymakeDemo", "Writing Pymake Projects")
    start = time.clock()
    PymakeWriter.write(projects)
    end = time.clock()
    pylogger.info("PymakeDemo", "Wrote {0} project files in {1} seconds:".format(len(projects), end - start))

    # Interpreters
    interpreters = set(i for p in projects for i in p.PythonInterpreters)
    pylogger.info("PymakeDemo", "Registering Pythong Interpreters.")
    start = time.clock()
    for i in interpreters:
        i.register()
    end = time.clock()
    pylogger.info("PymakeDemo", "Registered {0} interpreters in {1} seconds:".format(len(interpreters), end - start))

    return 0

if __name__ == "__main__":
    # To use PymakeDemo as a package we need to append the sys.path before executing main
    filePath = os.path.dirname( os.path.realpath(__file__) )
    for path in [os.path.normpath(p) for p in [os.path.join( filePath, '..'), os.path.join( filePath, '..', '..', '..')] if p not in sys.path]:
        sys.path.append(path)

    sys.exit(main(sys.argv))
