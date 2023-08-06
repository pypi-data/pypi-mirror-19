# -*- coding: utf-8 -*-
"""
This module handle finding the be engine dll's
"""

# ---------------------------------------------------------------------------- #
# Include
# ---------------------------------------------------------------------------- #
import sys
import os
import logging

if sys.version_info < (3, 0):
    # python2
    import _winreg as winreg
else:
    # python3
    import winreg

# ---------------------------------------------------------------------------- #
# Constants
# ---------------------------------------------------------------------------- #
ENGINE_DLLS = ('Be15Eng.dll', 'Be10Eng.dll')
REG_KEY_TARGET_PATH = r'SOFTWARE\Wow6432Node\SBi'  # HKLM
REG_KEY_INSTALL_DIR_TARGET = 'InstallDir'  # The name of the registry value containing the install location


# ---------------------------------------------------------------------------- #
# Functions
# ---------------------------------------------------------------------------- #
def find_engine_location():
    # type: () -> str
    """
    This function tries to locate the newest availabe calculation engine.
    :return: path to dll if sucessessfull else None
    """
    # Check current working dir
    res = check_dir(os.getcwd())
    if res is not None:
        return res
    # Check registry
    res = find_newest_engine_from_registry()
    if res is not None:
        return res
    # Failure
    return None


def check_dir(dir_path, engine_file_names=ENGINE_DLLS):
    # type: (str, list) -> str
    """
    This function checks whether the engine dll is located in the target directory
    :return: If found a string containing the path to the dll is returned else None
    """
    # Assert that dir_path is a path to a directory
    assert os.path.isdir(dir_path)
    # Iterate all possibilities
    for dll in engine_file_names:
        path = os.path.abspath(os.path.join(dir_path, dll))
        if os.path.exists(path):
            return path
    # If we got here we had no success finding the engine
    return None


def find_all_engines_from_registry():
    # type: (list) -> [str]
    """
    This function returns all detected engine locations
    :return: returns a list of all detected install locations
    """
    try:
        dir_paths = [path for path in scan_sub_keys(REG_KEY_TARGET_PATH) if os.path.exists(path)]
        dll_paths = list()
        for dir_path in dir_paths:
            path = check_dir(dir_path)
            if path is not None:
                dll_paths.append(path)
        return dll_paths
    except FileNotFoundError as Ex:
        logging.error(Ex)
        return []


def find_newest_engine_from_registry():
    # type: () -> str
    """
    This function checks the registry for possible location of the engines and selected the newest
    :return: If found a string containing the path to the installation directory is returned else None
    """
    engines = find_all_engines_from_registry()
    if len(engines) == 0:
        return None
    engines.sort()
    return engines[-1]


def scan_sub_keys(reg_key_path):
    # type: (str) -> [str]
    """
    This function calls a scan on the target reg key and recursively scans the sub keys
    :param reg_key_path: the target registry key object
    :return: returns a list of all detected install locations
    """
    # Detected paths
    paths = []
    # Open key
    reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_key_path, 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
    # Scan the current key
    res = scan_reg_key_for_values(reg_key)
    if res is not None:
        paths.append(res)
    # Iterate the sub keys
    try:
        index = 0
        while True:
            # Get name of key
            name = winreg.EnumKey(reg_key, index)
            # Construct new path
            new_reg_key_path = r'{}\{}'.format(reg_key_path, name)
            # Handle new key
            res_list = scan_sub_keys(new_reg_key_path)
            paths = paths + res_list
            # Increment index
            index += 1
    except OSError:
        # We receive this exception when there are no more keys
        pass
    # Return
    return paths


def scan_reg_key_for_values(reg_key):
    # type: () -> str
    """
    This function scan the target key for the value of the install location of be10/15 installations
    :param reg_key: the target registry key object
    :return: If found a string containing the path to the installation directory is returned else None
    """
    try:
        # Iterate values
        index = 0
        while True:
            # Get name of value
            name, value, type = winreg.EnumValue(reg_key, index)
            # Check if we have a match
            if name == REG_KEY_INSTALL_DIR_TARGET:
                return value
            # Incrment index
            index += 1
    except OSError:
        # We receive this exception when there are no more values
        pass
    return None
