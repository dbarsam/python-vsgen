# -*- coding: utf-8 -*-
"""
Main __init__.py for the vsgen package
"""
import pkg_resources
try:
    pkg = pkg_resources.get_distribution("vsgen")
    __version__ = pkg.version
except pkg_resources.DistributionNotFound:
    __version__ = "0.0.0.0"

from vsgen.solution import VSGSolution
from vsgen.register import VSGRegisterable, VSGRegisterCommand
from vsgen.writer import VSGWriter, VSGWritable, VSGWriteCommand
from vsgen.suite import VSGSuite
from vsgen.ptvs.interpreter import PTVSInterpreter
from vsgen.ptvs.project import PTVSProject
from vsgen.util.logger import VSGLogger
from vsgen.util.timer import VSGTimer
from vsgen.util.config import VSGConfigParser

__all__ = [
    'VSGSolution',
    'VSGRegisterable',
    'VSGRegisterCommand',
    'VSGWriter',
    'VSGWritable',
    'VSGWriteCommand',
    'VSGSuite',
    'PTVSInterpreter',
    'PTVSProject',
    'VSGLogger',
    'VSGTimer',
    'VSGConfigParser'
]
