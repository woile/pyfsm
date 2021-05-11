from .exceptions import AbortTransition, InvalidTransition

__all__ = ["FiniteStateMachineMixin", "BaseFiniteStateMachineMixin"]


class BaseFiniteStateMachineMixin:
    """Base Mixin to add a state_machine behavior.

    Represents the state machine for the object.

    The states and transitions should be specified in the following way:

    .. code-block:: python

        state_machine = {
           'some_state': '__all__'
           'another_state': ('some_state', 'one_more_state')
           'one_more_state': None
        }

    Requires the implementation of :code:`current_state` and :code:`set_state`
    """

    state_machine = None

    def current_state(self):
        """Returns the current state in the FSM."""
        raise NotImplementedError("Subclass must implement this method!")

    def set_state(self, state):
        """Update the internal state field.

        :param state: type depends on the definition of the states.
        :type state: str or int
        """
        raise NotImplementedError("Subclass must implement this method!")

    def can_change(self, next_state):
        """Validates if the next_state can be executed or not.

        It uses the state_machine attribute in the class.
        """
        valid_transitions = self.get_valid_transitions()

        if not valid_transitions:
            return False

        return next_state in valid_transitions

    def get_valid_transitions(self):
        """Return possible states to whom a product can transition.

        :returns: valid transitions
        :rtype: tuple or list
        """
        current = self.current_state()
        valid_transitions = self.state_machine[current]

        if valid_transitions == "__all__":
            return self.state_machine.keys()

        return self.state_machine[current]

    def on_before_change_state(self, previous_state, next_state, **kwargs):
        """Called before a state changes.

        :param previous_state: type depends on the definition of the states.
        :type previous_state: str or int
        :param next_state: type depends on the definition of the states.
        :type next_state: str or int
        """
        pass

    def on_change_state(self, previous_state, next_state, **kwargs):
        """Called after a state changes.

        :param previous_state: type depends on the definition of the states.
        :type previous_state: str or int
        :param next_state: type depends on the definition of the states.
        :type next_state: str or int
        """
        pass

    def change_state(self, next_state, **kwargs):
        """Performs a transition from current state to the given next state if
        possible.

        Callbacks will be exacuted before an after changing the state.
        Specific state callbacks will also be called if they are implemented
        in the subclass.

        :param next_state: where the state must go
        :type next_state: str or int
        :returns: new state.
        :rtype: str or int
        :raises InvalidTransition: If transitioning is not possible
        """
        previous_state = self.current_state()

        if not self.can_change(next_state):
            msg = "The transition from {0} to {1} is not valid".format(
                previous_state, next_state
            )
            raise InvalidTransition(msg)

        name = "pre_{0}".format(next_state)
        callback = getattr(self, name, None)
        if callback:
            try:
                callback(**kwargs)
            except AbortTransition:
                return previous_state

        self.on_before_change_state(previous_state, next_state, **kwargs)

        self.set_state(next_state)

        name = "post_{0}".format(next_state)
        callback = getattr(self, name, None)
        if callback:
            callback(**kwargs)

        self.on_change_state(previous_state, next_state, **kwargs)
        return next_state


class FiniteStateMachineMixin(BaseFiniteStateMachineMixin):
    """A drop in implementation. Ready to be used.

    Replace :code:`FIELD_NAME` in order to automatically retrieve or set
    from a different field.

    In order to use with django, just add a field :code:`state`
    or as defined in :code:`FIELD_NAME`
    and remember to use :code:`change_state` instead of simply assigning it
    """

    FIELD_NAME = "state"

    def current_state(self):
        return getattr(self, self.FIELD_NAME)

    def set_state(self, state):
        setattr(self, self.FIELD_NAME, state)
