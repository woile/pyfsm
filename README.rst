========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        | |codecov|
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/pyfsm/badge/?style=flat
    :target: https://readthedocs.org/projects/pyfsm
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/Woile/pyfsm.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/Woile/pyfsm

.. |codecov| image:: https://codecov.io/github/Woile/pyfsm/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/Woile/pyfsm

.. |version| image:: https://img.shields.io/pypi/v/python-fsm.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/python-fsm

.. |downloads| image:: https://img.shields.io/pypi/dm/python-fsm.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/python-fsm

.. |wheel| image:: https://img.shields.io/pypi/wheel/python-fsm.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/python-fsm

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/python-fsm.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/python-fsm

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/python-fsm.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/python-fsm


.. end-badges

Minimal state machine

* Free software: BSD license

Installation
============

::

    pip install fsmpy

Documentation
=============

https://pyfsm.readthedocs.org/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
