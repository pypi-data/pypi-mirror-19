======
``v2``
======

.. image:: https://travis-ci.org/solidsnack/v2.svg?branch=master
    :target: https://travis-ci.org/solidsnack/v2
.. image:: https://img.shields.io/pypi/v/v2.svg
    :target: https://pypi.python.org/pypi/v2
.. image:: https://img.shields.io/pypi/dd/v2.svg
    :target: https://pypi.python.org/pypi/v2

``v2`` provides for auto-versioning in an intuitive way.

From ``setup.py``:

.. code:: python

    from v2 import v2

    setup(
          # ...
          version=v2.from_git().from_file().imprint().version,
          # ...
          setup_requires=[..., 'v2', ...],
    )

From within your package root:

.. code:: python

    from v2 import v2

    __version__ = v2.from_pkg().from_git().from_default().version

From within your Sphinx ``conf.py``:

.. code:: python

    from v2 import v2

    # ...

    version = v2.from_file('../../VERSION').from_git().version

By default, ``v2`` looks for and writes to ``VERSION`` in the project root.
Consequently, a one-line ``MANIFEST.in`` is necessary:

.. code::

    include VERSION

----------
Precedence
----------

``v2`` allows you to control the order in which versions are found, simply by
call ``from_file``, ``from_git`` and ``from_pkg`` in the desired order. The
first one found is used; remaining searches are skipped. To obtain the version
value we use ``.version`` (it's always a string).

-------------------
Writing the Version
-------------------

The ``v2`` module's default interface object uses ``VERSION`` as the path to
its version file. With ``.from_file`` it reads from this file, if present;
with ``.imprint`` it writes to this file.
