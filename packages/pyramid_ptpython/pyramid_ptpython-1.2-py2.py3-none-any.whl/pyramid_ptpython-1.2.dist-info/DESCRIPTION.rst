pyramid_ptpython
================

A `ptpython <https://github.com/jonathanslenders/ptpython/>`_ and ``ptipython`` plugin
for `pyramid <http://www.pylonsproject.org/>`_ pshell.


Installation
------------

Install from PyPI using ``pip`` or ``easy_install``.

.. code-block:: bash

    $ pip install pyramid_ptpython


You can also add the ``ipython`` dependency for ``ptipython``:

.. code-block:: bash

    $ pip install pyramid_ptpython[ipython]


Usage
-----

``ptipython`` gets auto-selected if it is the only shell installed for pyramid.

.. code-block::

    $ pshell development.ini


To select a specific shell you can simply pass ``ptpython`` or ``ptipython`` as
shell argument to pyramids ``pshell``.

.. code-block::

    $ pshell -p ptpython development.ini


Or define ``default_shell`` in the ``pshell`` section of your ini-file like:

.. code-block::

    [pshell]
    default_shell = ptpython


1.2
---

- Support custom ptpython config
- Use global ptpython history
- Fix autocomplete

1.1
---

- Minimum pyramid version required is > 1.6a2
- ``pyramid.pshell`` is now ``pyramid.pshell_runner`` see: https://github.com/Pylons/pyramid/pull/2012


1.0
---

- First release


