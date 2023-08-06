cmdvars
=======

| Read environment variables defined in a shell script into Python.
| This library uses the shell to get variable values, and handles
  multiline variables.

Usage
=====

Given a shell file: myvars.env:

.. code:: shell

    #!/bin/bash
    export VAR1=1
    export VAR2="This
    is
    a
    multiline value"
    export VAR3=3
    NOT_EXPORTED=4

get\_vars
---------

.. code:: python

    >>> import shellvars 
    >>> shellvars.get_vars('myvars.env')
    {'VAR1': '1', 'VAR2': 'This\nis\na\nmultiline value', 'VAR3': '3' }

list\_vars
----------

Lists the variable names in the script.

.. code:: python

    >>> import shellvars 
    >>> shellvars.list_vars('myvars.env')
    ['VAR1', 'VAR2', 'VAR3']

This is equivalent to, but faster than

.. code:: python

    >>> shellvars.get_vars('myvars.env').keys()

