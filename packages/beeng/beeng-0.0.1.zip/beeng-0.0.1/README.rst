Be10/Be15 calculation engine wrapper for Python
===============================================

This Python library is designed to allow easy usage of the Be10 and Be15 calculation engines from Python.
Notice that the python interpreter must be 32 bit!

Example
-------

.. code:: python

    import beeng
    eng = beeng.Engine()
    model = eng.load_model(path)
    res_success, res_xml = eng.get_res_xml(model)
    key_success, key_xml = eng.get_key_xml(model)
    assert res_success == True
    assert key_success == True
