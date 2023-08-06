Be10/Be15 calculation engine wrapper for Python
===============================================

This Python library is designed to allow easy usage of the Be10 and Be15 calculation engines from Python.
Notice that the python interpreter must be 32 bit!

Install
-------

From the command line:

.. code:: bash
pip install beeng

Or

.. code:: bash
py -m pip install beeng

Example
-------

.. code:: python

    import beeng
    eng = beeng.Engine()
    model = eng.load_model('PATH_TO_YOUR_PROJECT_XML')
    res_success, res_xml = eng.get_res_xml(model)
    key_success, key_xml = eng.get_key_xml(model)
    assert res_success == True
    assert key_success == True

See the example directory for more options.

Engine parameters
-----------------

The following table shows that arguments that can be given to the Engine class.

========================== ======  ==================================================================================================================
 Argument                   Type    Comment
========================== ======  ==================================================================================================================
 be_eng_dll_path            str     The path to the Be engine DLL. If set to None beeng will attempt to auto find the dll.
 buffer_size                int     The number of bytes used for the results buffer
 uk_flag                    int     Control the language of the results. 0 = danish, 1 = english.
 check_for_valid_license    bool    If set to true beeng will check if a valid license is available. Only works from version 8.17.1.17 and forward.
========================== ======  ==================================================================================================================

Notice that the calculation engine always check for a valid license so check_for_valid_license is only a help to detect the problem.
If check_for_valid_license is set to false then the engine will simply fail to return results when no valid license is available.

Supported functions
-------------------

The following functions from the DLL can be used:

==================== ============= ===================================================================================================================================
 Function             Return        Comment
==================== ============= ===================================================================================================================================
 get_key_xml          (bool, str)   The bool indicates success and the str contains the key xml data
 get_res_xml          (bool, str)   The bool indicates success and the str contains the results xml data
 get_summer_comfort   (bool, str)   The bool indicates success and the str contains the summer comfort temperature xml data for each hour of every day the whole year
 is_license_valid     bool          The bool indicates if a valid license is available (True = valid license) (Supported from version 8.17.1.17 and forward)
==================== ============= ===================================================================================================================================

