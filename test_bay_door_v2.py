import unittest

from bay_door_v2 import *
from test_helpers import *

# Define expected behavior
expected_transitions_by_state = namify([
    ['', CLOSING_STATE, 'ex', 'ex'],  # for OPEN_STATE
    [OPENING_STATE, '', 'ex', 'ex'],  # for CLOSED_STATE
    ['', CLOSING_STATE, OPEN_STATE, 'ex'],  # for OPENING_STATE
    [OPENING_STATE, '', 'ex', CLOSED_STATE]  # for CLOSING_STATE
], STATE_NAMES)

class BayDoorV2(unittest.TestCase):

    def test_pre_hooks(self):
        sm_deny = StateMachine(lambda x, y, z: False)
        for state in range(len(STATE_NAMES)):
            for event in range(len(EVENT_NAMES)):
                if len(expected_transitions_by_state[state][event]) > 2:
                    # A handler that denies the transition should prevent changes.
                    sm_deny.state = state # artificially alter state
                    sm_deny.handle(event)
                    self.assertEquals(state, sm_deny.state)

    def test_post_hooks(self):
        class Counter:
            def __init__(self): self.count = 0
            def __call__(self, sm, state, event): self.count += 1
        counter = Counter()
        sm = StateMachine(post = counter)
        for state in range(len(STATE_NAMES)):
            for event in range(len(EVENT_NAMES)):
                if len(expected_transitions_by_state[state][event]) > 2:
                    # A handler that denies the transition should prevent changes.
                    sm.state = state # artificially alter state
                    sm.handle(event)
        self.assertEquals(counter.count, 6)

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