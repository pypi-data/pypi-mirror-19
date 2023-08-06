36-chambers
=====================================================================

36-chambers is a Python Library which adds common reversing methods and
functions for Binary Ninja. The library is designed to be used within Binary
Ninja in the Python console.

Installation
------------

Use pip to install or upgrade 36-chambers::

    $ pip install 36-chambers [--upgrade]

Quick Example
-------------

Find and print all blocks with a "push" instruction:

.. code-block :: python

    from chambers import Chamber

    c = Chamber(bv=bv)
    c.instructions('push')

Documentation
-------------

For more information you can find documentation on readthedocs_.

.. _readthedocs: https://36-chambers.readthedocs.org
