import unittest

from airlock import *
from test_helpers import *

# Define expected behavior
expected_transitions_by_state = namify([
    [DEPRESSURIZING_STATE, OPENING_INNER_STATE, 'ex', 'ex', 'ex', 'ex', 'ex', 'ex'],  # for CLOSED_PRESSURIZED_STATE
    [OPENING_OUTER_STATE, PRESSURIZING_STATE, 'ex', 'ex', 'ex', 'ex', 'ex', 'ex'],  # for CLOSED_DEPRESSURIZED_STATE
    ['', CLOSING_OUTER_STATE, 'ex', 'ex', OUTER_OPEN_HOSTILE_STATE, 'ex', 'ex', 'ex'],  # for OPENING_OUTER_STATE
    [CLOSING_INNER_STATE, '', 'ex', 'ex', 'ex', INNER_OPEN_STATE, 'ex', 'ex'],  # for OPENING_INNER_STATE
    [OPENING_OUTER_STATE, '', 'ex', 'ex', 'ex', 'ex', 'ex', 'ex'],  # for CLOSING_OUTER_STATE
    ['', OPENING_INNER_STATE, 'ex', 'ex', 'ex', 'ex', 'ex', 'ex'],  # for CLOSING_INNER_STATE
    [DEPRESSURIZING_STATE, '', 'ex', 'ex', 'ex', 'ex', 'ex', 'ex'],  # for PRESSURIZING_STATE
    [PRESSURIZING_STATE, PRESSURIZING_STATE, 'ex', 'ex', 'ex', 'ex', 'ex', 'ex'],  # for DEPRESSURIZING_STATE
    [CLOSING_INNER_STATE, '', 'ex', 'ex', 'ex', 'ex', 'ex', 'ex'],  # for INNER_OPEN_STATE
    ['', CLOSING_OUTER_STATE, 'ex', 'ex', 'ex', 'ex', 'ex', 'ex'],  # for OUTER_OPEN_FRIENDLY_STATE
    ['', CLOSING_OUTER_STATE, 'ex', 'ex', 'ex', 'ex', 'ex', 'ex'],  # for OUTER_OPEN_HOSTILE_STATE
], STATE_NAMES)

class Airlock(unittest.TestCase):

    def test_matrix(self):
        sm = StateMachine(lambda x: True)

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