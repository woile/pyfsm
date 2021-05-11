=====
Usage
=====

1. Define in a class the :code:`state_machine`
2. Initialize :code:`state`, either with a value, using :code:`__init__` or as a django field
3. Add hooks:

+------------------------+-------------------------------------------------------------------------------------------------------------+
| Method                 | Description                                                                                                 |
+------------------------+-------------------------------------------------------------------------------------------------------------+
| on_before_change_state | Before transitioning to the state                                                                           |
+------------------------+-------------------------------------------------------------------------------------------------------------+
| on_change_state        | After transitioning to the state, if no failure, runs for every state                                       |
+------------------------+-------------------------------------------------------------------------------------------------------------+
| pre_<state_name>       | Runs before a particular state, where :code:`state_name` is the specified name in the :code:`state_machine` |
+------------------------+-------------------------------------------------------------------------------------------------------------+
| post_<state_name>      | Runs after a particular state, where :code:`state_name` is the specified name in the :code:`state_machine`  |
+------------------------+-------------------------------------------------------------------------------------------------------------+

This hooks will receive any extra argument given to :code:`change_state`


E.g:

Running :code:`m.change_state('pending', name='john')` will trigger :code:`pre_pending(name='john')`

Raising AbortTransition in `pre_<state_name>` method will result in no state change and `on_before_change_state` not called.

In your code
------------


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
