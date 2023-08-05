.. image:: https://travis-ci.org/filwaitman/pyrecursive.svg?branch=master
    :target: https://travis-ci.org/filwaitman/pyrecursive


pyrecursive
===========

Have you ever needed to transform a :code:`whatever python object` in depth? So this one is for you. =]

This library runs on both Python 2 and Python 3 (tested on 2.7 and 3.5, precisely).


Installation:
-------------

.. code:: bash

    pip install pyrecursive


Usage:
-------------

.. code:: python

    from pyrecursive import pyrecursive

    def double(obj):
        return x * 2

    pyrecursive(42, double)
    # result: 84

    pyrecursive([1, 2, 3, [4, 5, [6], 7], 8, 9, 'x'], double)
    # result: [2, 4, 6, [8, 10, [12], 14], 16, 18, 'xx']

    pyrecursive({'hamster': [1, 2, 3, {'test': 42}]}, double)
    # result: {'hamster': [2, 4, 6, {'test': 84}]}

    # In order to transform dict keys in depth by setting transform_dict_keys variable to True (default: False).
    pyrecursive({'hamster': [1, 2, 3, {'test': 42}]}, double, transform_dict_keys=True)
    # result: {'hamsterhamster': [2, 4, 6, {'testtest': 84}]}

    # In order not to transform dict value in depth by setting transform_dict_values variable to False (default: True).
    pyrecursive({'hamster': [1, 2, 3, {'test': 42}]}, double, transform_dict_values=False)
    # result: {'hamster': [2, 4, 6, {'test': 42}]}

    # In order to define custom rules for each object type in depth by setting custom_rules variable.
    pyrecursive([1, 2, 3, 'banana'], double, custom_rules={int: lambda x: x * 5})
    # result: [5, 10, 15, 'bananabanana'] (multiplied by 5 when int, multiplied by 2 otherwise)


Contribute
----------
Did you think in some interesting feature, or have you found a bug? Please let me know!

Of course you can also download the project and send me some `pull requests <https://github.com/filwaitman/pyrecursive/pulls>`_. Please keep in mind that (1) we do follow pep8, (2) our line-length is 120 chars and (3) your changes must be compatible with Python 2.7 and Python 3.5.

You can send your suggestions by `opening issues <https://github.com/filwaitman/pyrecursive/issues>`_.

You can contact me directly as well. Take a look at my contact information at `http://filwaitman.github.io/ <http://filwaitman.github.io/>`_ (email is preferred rather than mobile phone).
