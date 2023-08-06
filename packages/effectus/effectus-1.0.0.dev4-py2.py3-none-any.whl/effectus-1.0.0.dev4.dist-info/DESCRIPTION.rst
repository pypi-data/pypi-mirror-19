effectus - A cause-effect library
=================================

.. image:: https://img.shields.io/pypi/v/effectus.svg
  :target: https://pypi.python.org/pypi/effectus
  :alt: Pypi version

.. image:: https://img.shields.io/pypi/pyversions/effectus.svg
  :target: https://pypi.python.org/pypi/effectus
  :alt: Python versions

.. image:: https://img.shields.io/appveyor/ci/hyllos/effectus-python/default.svg
  :target: https://ci.appveyor.com/project/hyllos/effectus-python
  :alt: Windows Built Status

.. image:: https://img.shields.io/codecov/c/bitbucket/hyllos/effectus-python/default.svg
  :target: https://codecov.io/bb/hyllos/effectus-python
  :alt: Code coverage 

What?
-----

You provide it with a series of numbers.
It tells you whether a pareto distribution is present.

Why?
----

``Mean``, ``Median`` and ``Most likely value`` regularly hide that a
minority of causes provokes a majority of effects.

`The Fallacy of the Arithmetic Mean <http://docs.unterschied.cc/effectus-python/fallacy.html>`_ explains the situation in-depth.

How?
----

First, install it:

.. code-block:: bash

    $ pip3 install effectus

Then, in your Python shell do:

.. code-block:: python

   from effectus import Effects
   Effects([789, 621, 109, 65, 45, 30, 27, 15, 12, 9])
   <pareto present [0.707]: 1/5 causes => 4/5 effects [total ∆: 2.3 %]>

If you want 80% of results, you need only 20% of causes.

`» Documentation <http://docs.unterschied.cc/effectus-python>`_
---------------------------------------------------------------


