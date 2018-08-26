=====
Usage
=====

To use Python Finite State Machine in a project::

    import fsm


Then add the Mixin to any class where the state machine is required.

.. code:: python

  class Foo(fsm.FiniteStateMachineMixin):

      state_machine = {
          'my_first_state': '__all__',
          'my_state': ('my_second_state',),
          'my_second_state': ('my_state', 'my_second_state', 'last_state'),
          'last_state': None
      }

      state = 'my_first_state'


Instanciate the class and use it. Remember that in order to work as intended, :code:`change_state`
must be used to transition from one state to the other.

.. code::

  >>> foo = Foo()

  >>> foo.current_state()
  'my_first_state'

  >>> foo.change_state('my_state')
  'my_state'

  >>> foo.current_state()
  'my_state'

  >>> foo.can_change('last_state')
  False

  >>> foo.get_valid_transitions()
  ('my_second_state',)



You can also use :code:`BaseFiniteStateMachineMixin` for more flexibility.
Implementing :code:`current_state` and :code:`set_state` is required.
Doing this allows using more complex behavior, but it is **not recommended**.
