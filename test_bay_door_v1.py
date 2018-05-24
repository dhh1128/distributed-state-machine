import unittest

from bay_door_v1 import *

class BayDoorV1Case(unittest.TestCase):

    def check_transition(self, sm, event, trans):
        start_state = STATE_NAMES[sm.state]
        if trans:
            expected = trans
        else:
            expected = STATE_NAMES[sm.state]
        try:
            sm.handle(event)
            actual = STATE_NAMES[sm.state]
        except Exception:
            actual = 'ex'
        if actual != expected:
            return "%s + %s != %s -- new state = %s instead" % (start_state, EVENT_NAMES[event], expected, actual)

    def test_matrix(self):
        expected_transitions_by_state = [
            ['', STATE_NAMES[CLOSING_STATE], 'ex', 'ex'], # for OPEN_STATE
            [STATE_NAMES[OPENING_STATE], '', 'ex', 'ex'],  # for CLOSED_STATE
            ['', STATE_NAMES[CLOSING_STATE], STATE_NAMES[OPEN_STATE], 'ex'],  # for OPENING_STATE
            [STATE_NAMES[OPENING_STATE], '', 'ex', STATE_NAMES[CLOSED_STATE]]  # for CLOSING_STATE
        ]
        sm = StateMachine()

        problems = []
        # Artificially place state machine in a state, and test every event to see if
        # it triggers the expected transition.
        for state in range(len(STATE_NAMES)):
            for event in range(len(EVENT_NAMES)):
                sm.state = state
                outcome = self.check_transition(sm, event, expected_transitions_by_state[state][event])
                if outcome:
                    problems.append(outcome)
        if problems:
            msg = '\n'.join(problems)
            self.fail(msg)

if __name__ == '__main__':
    unittest.main()