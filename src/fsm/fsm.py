from .exceptions import InvalidTransition


__all__ = ['FiniteStateMachineMixin']


class FiniteStateMachineMixin:
    """Mixins which adds the behavior of a state_machine.

    Represents the state machine for the object.

    The states and transitions should be specified in the following way:

    state_machine = {
       'some_state': '__all__'
       'another_state': ('some_state', 'one_more_state')
       'one_more_state': None
    }
    """

    state_machine = None

    def current_state(self):
        """Returns the current state in the FSM."""
        raise NotImplementedError('Subclass must implement this method!')

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

        if valid_transitions == '__all__':
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
        """Performs a transition from current state to the given next state if possible.

        Callbacks will be exacuted before an after changing the state.
        Specific state callbacks will also be called if they are implemented
        in the subclass.

        :param next_state: where the state must go
        :type next_state: str or int
        :raises InvalidTransition: If transitioning is not possible
        """
        previous_state = self.current_state()

        if self.can_change(next_state):
            name = 'on_before_{0}_callback'.format(next_state)
            callback = getattr(self, name, None)
            if callback:
                callback(**kwargs)

            self.on_before_change_state(previous_state, next_state, **kwargs)

            self.state = next_state

            name = 'on_{0}_callback'.format(next_state)
            callback = getattr(self, name, None)
            if callback:
                callback(**kwargs)

            self.on_change_state(previous_state, next_state, **kwargs)

        else:
            msg = "The transition from {0} to {1} is not valid".format(previous_state,
                                                                       next_state)
            raise InvalidTransition(msg)
