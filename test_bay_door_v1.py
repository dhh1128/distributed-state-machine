import unittest

from bay_door_v1 import *

# Define expected behavior
expected_transitions_by_state = [
    ['', STATE_NAMES[CLOSING_STATE], 'ex', 'ex'],  # for OPEN_STATE
    [STATE_NAMES[OPENING_STATE], '', 'ex', 'ex'],  # for CLOSED_STATE
    ['', STATE_NAMES[CLOSING_STATE], STATE_NAMES[OPEN_STATE], 'ex'],  # for OPENING_STATE
    [STATE_NAMES[OPENING_STATE], '', 'ex', STATE_NAMES[CLOSED_STATE]]  # for CLOSING_STATE
]

class BayDoorV1(unittest.TestCase):

    def test_matrix(self):
        sm = StateMachine()

        problems = []
        # Artificially place state machine in a state, and test every event to see if
        # it triggers the expected transition.
        for state in range(len(STATE_NAMES)):
            for event in range(len(EVENT_NAMES)):
                sm.state = state
                outcome = check_transition(sm, event, expected_transitions_by_state[state][event])
                if outcome:
                    problems.append(outcome)
        if problems:
            msg = '\n'.join(problems)
            self.fail(msg)

def check_transition(sm, event, trans):
    start_state = STATE_NAMES[sm.state]
    expected = trans if trans else STATE_NAMES[sm.state]
    try:
        sm.handle(event)
        actual = STATE_NAMES[sm.state]
    except Exception:
        actual = 'ex'
    if actual != expected:
        return "%s + %s != %s -- new state = %s instead" % (start_state, EVENT_NAMES[event], expected, actual)

if __name__ == '__main__':
    unittest.main()