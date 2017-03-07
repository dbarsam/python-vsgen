# -*- coding: utf-8 -*-
"""
This module provides all functionality for extending Python's entrypoints functionality.
"""

import os
import glob
import configparser
import pkg_resources


def entrypoints(section):
    """
    Returns the Entry Point for a given Entry Point section.

    :param str section: The section name in the entry point collection
    :returns:  A dictionary of (Name, Class) pairs stored in the entry point collection.
    """
    return {ep.name: ep.load() for ep in pkg_resources.iter_entry_points(section)}


def entrypoint(section, option):
    """
    Returns the the entry point object given a section, option pair.

    :param str section: The section name in the entry point collection
    :param str option: The option name in the entry point collection
    :return:  The entry point object if available.
    """
    try:
        return entrypoints(section)[option]
    except KeyError:
        raise KeyError('Cannot resolve type "{}" to a recognised vsgen "{}" type.'.format(option, section))
