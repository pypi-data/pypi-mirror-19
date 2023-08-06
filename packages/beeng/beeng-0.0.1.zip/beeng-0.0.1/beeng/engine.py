# -*- coding: utf-8 -*-
"""
This module handles the calls to the calculation engine
"""

# ---------------------------------------------------------------------------- #
# Include
# ---------------------------------------------------------------------------- #
import sys
import os
import ctypes
import logging
import platform
import beeng.finder


# ---------------------------------------------------------------------------- #
# Constants
# ---------------------------------------------------------------------------- #
TEXT_CODEC = 'latin-1'


# ---------------------------------------------------------------------------- #
# Class
# ---------------------------------------------------------------------------- #
class Engine:

    def __init__(self, be_eng_dll_path=None, buffer_size=1000000, uk_flag=0, check_for_valid_license=True):
        # type: (str, int, int, bool) -> None
        """
        Constructor
        :param be_eng_dll_path: The path to the be calculation engine dll (If set to None we try to automatically find it)
        :param buffer_size: The size for the result buffer string (If smaller than the actual result, data will be lost!)
        :param uk_flag: Controls whether the results are in english (1) or danish (0)
        :param check_for_valid_license: If this is set to true we check if a valid license is installed when loading the engine
        """
        # Fields
        self.be_eng_dll_path = os.path.abspath(be_eng_dll_path)
        self.buffer_size = buffer_size
        self.uk_flag = uk_flag
        self.check_for_valid_license = check_for_valid_license
        self.old_path = os.environ['PATH']
        self.engine = None
        # Asserts
        assert self.uk_flag in (0, 1)
        # Find location if be_eng_dll_path is none
        if be_eng_dll_path is None:
            logging.debug('No path specified for the engine DLL. Trying to find the newest engine.')
            self.be_eng_dll_path = beeng.finder.find_engine_location()
            logging.debug('Found engine at: {}'.format(self.be_eng_dll_path))
            assert self.be_eng_dll_path is not None, 'The calculation engine could not automatically be found'
        # Load engine
        self.load_engine(self.be_eng_dll_path)

    def load_engine(self, path):
        # type: (str) -> None
        """
        This function loads the calculation engine
        """
        # Check interpreter
        self.check_interpreter_bits()
        # Save old paths
        self.old_path = os.environ['PATH']
        # Get directory
        dir_name, file_name = os.path.split(path)
        # Change path (Used so we can load the dll from a directory different from cwd)
        os.environ['PATH'] = dir_name + ';' + os.environ['PATH']
        # Load engine
        self.engine = ctypes.windll.LoadLibrary(file_name)
        # Check license if valid
        if self.check_for_valid_license == True:
            is_valid = self.is_license_valid()
            if is_valid == False:
                raise Exception('Missing a valid license for the DLL')

    def unload_engine(self):
        """
        This function unloads the calculation engine
        """
        os.environ['PATH'] = self.old_path
        del self.engine
        self.engine = None

    def check_interpreter_bits(self):
        """
        This function ensures that the python interpreter is running in 32 bit mode
        """
        if platform.architecture()[0] != '32bit':
            raise Exception('This package is only compatible with 32 bit python!')

    @staticmethod
    def load_model(model_path):
        # type: (str) -> None
        """
        Opens a xml model file and stores it in a c compatible string buffer (used for returned results)
        :param model_path: Path to model file
        :return: Project XML C string buffer
        """
        f = open(model_path, 'r')
        p_model = f.read()
        f.close()
        if sys.version_info < (3, 0):
            # python2
            return ctypes.create_string_buffer(p_model)
        else:
            # python3
            return ctypes.create_string_buffer(p_model.encode(TEXT_CODEC))

    def get_key_xml(self, model_string_buffer):
        # type: (str) -> (bool, str)
        """
        Gets the key results
        :param model_string_buffer: The model returned by the load_model function
        :return: success status (false = failure), XML document C string buffer
        """
        # Prepare arguments
        mem = ctypes.create_string_buffer(self.buffer_size)
        status = ctypes.c_int(ctypes.sizeof(mem))
        uk = ctypes.c_int(self.uk_flag)
        # Call function
        res_code = self.engine.Be06Keys(model_string_buffer, mem, ctypes.byref(status), uk)
        # Decode result
        key_xml = mem.raw.decode(TEXT_CODEC).strip('\0\n')
        # Return result
        return res_code != 0, key_xml

    def get_res_xml(self, model_string_buffer):
        # type: (str) -> (bool, str)
        """
        Gets the full results
        :param model_string_buffer: The model returned by the load_model function
        :return: success status (false = failure), XML document C string buffer
        """
        # Prepare arguments
        mem = ctypes.create_string_buffer(self.buffer_size)
        status = ctypes.c_int(ctypes.sizeof(mem))
        uk = ctypes.c_int(self.uk_flag)
        # Call function
        res_code = self.engine.Be06Res(model_string_buffer, mem, ctypes.byref(status), uk)
        # Decode result
        key_xml = mem.raw.decode(TEXT_CODEC).strip('\0\n')
        # Return result
        return res_code != 0, key_xml

    def is_license_valid(self):
        # type: () -> bool
        """
        This function checks whether a valid license is found
        :return:
        """
        # Call function
        res_code = self.engine.IsLicenseValid()
        # Return result
        return res_code == 0
