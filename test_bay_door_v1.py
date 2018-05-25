import unittest

from bay_door_v1 import *
from test_helpers import *

# Define expected behavior
expected_transitions_by_state = namify([
    ['', CLOSING_STATE, 'ex', 'ex'],  # for OPEN_STATE
    [OPENING_STATE, '', 'ex', 'ex'],  # for CLOSED_STATE
    ['', CLOSING_STATE, OPEN_STATE, 'ex'],  # for OPENING_STATE
    [OPENING_STATE, '', 'ex', CLOSED_STATE]  # for CLOSING_STATE
], STATE_NAMES)

class BayDoorV1(unittest.TestCase):

    def test_matrix(self):
        sm = StateMachine()

        problems = []
        # Artificially place state machine in a state, and test every event to see if
        # it triggers the expected transition.
        for state in range(len(STATE_NAMES)):
            for event in range(len(EVENT_NAMES)):
                sm.state = state
                transition = expected_transitions_by_state[state][event]
                outcome = check_transition(sm, event, transition, STATE_NAMES, EVENT_NAMES)
                if outcome:
                    problems.append(outcome)
        if problems:
            msg = '\n'.join(problems)
            self.fail(msg)

if __name__ == '__main__':
    unittest.main()