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
      - |version| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/pyfsm/badge/?style=flat
    :target: https://readthedocs.org/projects/pyfsm
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/Woile/pyfsm.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/Woile/pyfsm

.. |codecov| image:: https://codecov.io/github/Woile/pyfsm/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/Woile/pyfsm

.. |version| image:: https://img.shields.io/pypi/v/fsmpy.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/fsmpy

.. |wheel| image:: https://img.shields.io/pypi/wheel/fsmpy.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/fsmpy

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/fsmpy.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/fsmpy

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/fsmpy.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/fsmpy


.. end-badges

Minimal state machine

* Free software: BSD license

.. contents::
    :depth: 2

Usage
=====

.. code-block:: python

    import fsm

    class MyTasks(fsm.FiniteStateMachineMixin):
        """An example to test the state machine.

        Contains transitions to everywhere, nowhere and specific states.
        """

        state_machine = {
            'created': '__all__',
            'pending': ('running',),
            'running': ('success', 'failed'),
            'success': None,
            'failed': ('retry',),
            'retry': ('pending', 'retry'),
        }

        def __init__(self, state):
            """Initialize setting a state."""
            self.state = state

        def on_before_pending(self):
            print("I'm going to a pending state")

::

    In [4]: m = MyTasks(state='created')

    In [5]: m.change_state('pending')
    I'm going to a pending state
    Out[5]: 'pending'

    In [6]: m.change_state('failed')
    ---------------------------------------------------------------------------
    InvalidTransition                         Traceback (most recent call last)
    <ipython-input-6-71d2461eee74> in <module>()
    ----> 1 m.change_state('failed')

    ~/pyfsm/src/fsm/fsm.py in change_state(self, next_state, **kwargs)
        90             msg = "The transition from {0} to {1} is not valid".format(previous_state,
        91                                                                        next_state)
    ---> 92             raise InvalidTransition(msg)
        93
        94         name = 'pre_{0}'.format(next_state)

    InvalidTransition: The transition from pending to failed is not valid


There are hooks that can be included before a state transition happens and after.

fsm will look for these functions

::

    pre_<state_name>
    post_<state_name>

And will give them any extra argument given to :code:`change_state`

E.g:

Running :code:`m.change_state('pending', name='john')` will trigger :code:`pre_pending(name='john')`


Installation
============

::

    pip install fsmpy


Django integration
==================

.. code-block:: python

    import fsm
    from django.db import models


    class MyModel(models.Model, fsm.FiniteStateMachineMixin):
        """An example to test the state machine.

        Contains transitions to everywhere, nowhere and specific states.
        """

        CHOICES = (
            ('created', 'CREATED'),
            ('pending', 'PENDING'),
            ('running', 'RUNNING'),
            ('success', 'SUCCESS'),
            ('failed', 'FAILED'),
            ('retry', 'RETRY'),
        )

        state_machine = {
            'created': '__all__',
            'pending': ('running',),
            'running': ('success', 'failed'),
            'success': None,
            'failed': ('retry',),
            'retry': ('pending', 'retry'),
        }

        state = models.CharField(max_length=30, choices=CHOICES, default='created')

        def on_change_state(self, previous_state, next_state, **kwargs):
            self.save()


Documentation
=============

https://pyfsm.readthedocs.org/

Development
===========

To run the tests run::

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
