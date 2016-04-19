import unittest
import fsm


class ProgramExecution(fsm.FiniteStateMachineMixin):
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

    def current_state(self):
        """Overriden."""
        return self.state


class TestStateMachine(unittest.TestCase):

    def setUp(self):
        self.program_execution = ProgramExecution('created')

    def transition_anywhere(self):
        """Test when a state can go anywhere.

        Defined as __all__
        """
        state = self.program_execution.change_state('pending')
        assert state == 'pending'

    def test_successful_specific_transition(self):
        """Test a succesful state transition."""
        _ = self.program_execution.change_state('pending')
        state = self.program_execution.change_state('running')
        assert state == 'running'

    def test_failed_specific_transition(self):
        """Test a failed state transition."""
        _ = self.program_execution.change_state('pending')
        try:
            state = self.program_execution.change_state('success')
        except fsm.InvalidTransition:
            state = None
        assert state is None

    def test_succesful_transition_to_self(self):
        """Succesful transition from a state to the same state."""
        _ = self.program_execution.change_state('pending')
        _ = self.program_execution.change_state('running')
        _ = self.program_execution.change_state('failed')
        _ = self.program_execution.change_state('retry')
        state = self.program_execution.change_state('retry')
        assert state == 'retry'

    def test_failed_transition_to_self(self):
        """Succesful transition from a state to the same state."""
        _ = self.program_execution.change_state('pending')
        _ = self.program_execution.change_state('running')
        try:
            state = self.program_execution.change_state('running')
        except fsm.InvalidTransition:
            state = None
        assert state is None

    def test_failed_nowhere_transition_to_created(self):
        """Test that a nowhere transition always fails (created)."""
        _ = self.program_execution.change_state('pending')
        _ = self.program_execution.change_state('running')
        _ = self.program_execution.change_state('success')
        try:
            state = self.program_execution.change_state('created')
        except fsm.InvalidTransition:
            state = None
        assert state is None

    def test_failed_nowhere_transition_to_pending(self):
        """Test that a nowhere transition always fails (pending)."""
        _ = self.program_execution.change_state('pending')
        _ = self.program_execution.change_state('running')
        _ = self.program_execution.change_state('success')
        try:
            state = self.program_execution.change_state('pending')
        except fsm.InvalidTransition:
            state = None
        assert state is None

    def test_failed_nowhere_transition_to_running(self):
        """Test that a nowhere transition always fails (running)."""
        _ = self.program_execution.change_state('pending')
        _ = self.program_execution.change_state('running')
        _ = self.program_execution.change_state('success')
        try:
            state = self.program_execution.change_state('running')
        except fsm.InvalidTransition:
            state = None
        assert state is None

    def test_failed_nowhere_transition_to_success(self):
        """Test that a nowhere transition always fails (success)."""
        _ = self.program_execution.change_state('pending')
        _ = self.program_execution.change_state('running')
        _ = self.program_execution.change_state('success')
        try:
            state = self.program_execution.change_state('success')
        except fsm.InvalidTransition:
            state = None
        assert state is None

    def test_failed_nowhere_transition_to_failed(self):
        """Test that a nowhere transition always fails (failed)."""
        _ = self.program_execution.change_state('pending')
        _ = self.program_execution.change_state('running')
        _ = self.program_execution.change_state('success')
        try:
            state = self.program_execution.change_state('failed')
        except fsm.InvalidTransition:
            state = None
        assert state is None

    def test_failed_nowhere_transition_to_retry(self):
        """Test that a nowhere transition always fails (retry)."""
        _ = self.program_execution.change_state('pending')
        _ = self.program_execution.change_state('running')
        _ = self.program_execution.change_state('success')
        try:
            state = self.program_execution.change_state('retry')
        except fsm.InvalidTransition:
            state = None
        assert state is None
