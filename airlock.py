# Define states and events, including symbolic (numeric) constants and their friendly names.
STATE_NAMES = ['closed pressurized', 'closed depressurized', 'opening outer', 'opening inner', 'closing outer',
               'closing inner', 'pressurizing', 'depressurizing', 'inner open', 'outer open friendly',
               'outer open hostile']
for i in range(len(STATE_NAMES)):
    globals()[STATE_NAMES[i].upper().replace(' ', '_') + '_STATE'] = i
EVENT_NAMES = ['ask open outer', 'ask open inner', 'finished pressurizing', 'finished depressurizing',
               'finished opening outer', 'finished opening inner', 'finished closing outer', 'finished closing inner']
for i in range(len(EVENT_NAMES)):
    globals()[EVENT_NAMES[i].upper().replace(' ', '_') + '_EVENT'] = i

SENSOR_BAY_ENV_HOSTILE = 'bay env hostile?'

class StateMachine:

    def __init__(self, sensor_func, pre=None, post=None):
        self.state = CLOSED_PRESSURIZED_STATE
        self.goal = None
        self._sensor_func = sensor_func
        self._pre = pre
        self._post = post

    def handle(self, event):
        s = self.state
        if event == ASK_OPEN_OUTER_EVENT:
            if s in [OPENING_OUTER_STATE, OUTER_OPEN_FRIENDLY_STATE, OUTER_OPEN_HOSTILE_STATE]:
                return
            target_hostile = self._check_sensor(SENSOR_BAY_ENV_HOSTILE)
            old_goal = self.goal
            self.goal = OUTER_OPEN_HOSTILE_STATE if target_hostile else OUTER_OPEN_FRIENDLY_STATE
            if s == CLOSED_PRESSURIZED_STATE:
                self._transition_to(
                    DEPRESSURIZING_STATE if target_hostile else OPENING_OUTER_STATE, event)
            elif s == CLOSED_DEPRESSURIZED_STATE:
                self._transition_to(
                    OPENING_OUTER_STATE if target_hostile else PRESSURIZING_STATE, event)
            elif s in [OPENING_INNER_STATE, INNER_OPEN_STATE]:
                self._transition_to(CLOSING_INNER_STATE, event)
            elif s == CLOSING_OUTER_STATE:
                self._transition_to(OPENING_OUTER_STATE, event)
            elif s == CLOSING_INNER_STATE:
                pass
            elif s == PRESSURIZING_STATE:
                if old_goal != self.goal:
                    self._transition_to(DEPRESSURIZING_STATE, event)
            elif s == DEPRESSURIZING_STATE:
                if old_goal != self.goal:
                    self._transition_to(PRESSURIZING_STATE, event)
            else:
                raise AssertionError("Unhandled state %d" % s)
        elif event == ASK_OPEN_INNER_EVENT:
            if s in [OPENING_INNER_STATE, INNER_OPEN_STATE]:
                return
            self.goal = INNER_OPEN_STATE
            if s == CLOSED_PRESSURIZED_STATE:
                self._transition_to(OPENING_INNER_STATE, event)
            elif s == CLOSED_DEPRESSURIZED_STATE:
                self._transition_to(PRESSURIZING_STATE, event)
            elif s in [OPENING_OUTER_STATE, OUTER_OPEN_FRIENDLY_STATE, OUTER_OPEN_HOSTILE_STATE]:
                self._transition_to(CLOSING_OUTER_STATE, event)
            elif s == CLOSING_INNER_STATE:
                self._transition_to(OPENING_INNER_STATE, event)
            elif s in [PRESSURIZING_STATE, CLOSING_OUTER_STATE]:
                pass
            elif s == DEPRESSURIZING_STATE:
                self._transition_to(PRESSURIZING_STATE, event)
            else:
                raise AssertionError("Unhandled state %d" % s)
        else:
            if s == OPENING_OUTER_STATE and event == FINISHED_OPENING_OUTER_EVENT:
                target_hostile = self._check_sensor(SENSOR_BAY_ENV_HOSTILE)
                self._transition_to(OUTER_OPEN_HOSTILE_STATE if target_hostile else OUTER_OPEN_FRIENDLY_STATE, event)
                return
            elif s == OPENING_INNER_STATE and event == FINISHED_OPENING_INNER_EVENT:
                self._transition_to(INNER_OPEN_STATE, event)
                return
            elif (s == CLOSING_OUTER_STATE and event == FINISHED_CLOSING_OUTER_EVENT) or \
                    (s == CLOSING_INNER_STATE and event == FINISHED_CLOSING_INNER_EVENT) or \
                    (s == PRESSURIZING_STATE and event == FINISHED_PRESSURIZING_STATE) or \
                    (s == DEPRESSURIZING_STATE and event == FINISHED_DEPRESSURIZING_STATE):
                self._follow_goal(s)
                return
            raise AssertionError("Illegal event %s for state %s." % (EVENT_NAMES[event], STATE_NAMES[s]))

    def _check_sensor(self, sensor_name):
        if self._sensor_func:
            return self._sensor_func(sensor_name)

    def _follow_goal(self, event):
        if self.goal == INNER_OPEN_STATE:
            if event == FINISHED_PRESSURIZING:
                self._transition_to(OPENING_INNER_STATE, event)
            elif event == FINISHED_CLOSING_OUTER_EVENT:
                self._transition_to(PRESSURIZING_STATE, event)
            else:
                raise AssertionError("Unhandled case.")
        elif self.goal in [OUTER_OPEN_FRIENDLY_STATE, OUTER_OPEN_HOSTILE_STATE]:
            if event == FINISHED_DEPRESSURIZING:
                self._transition_to(OPENING_OUTER_STATE, event)
            elif event == FINISHED_CLOSING_INNER_EVENT:
                self._transition_to(DEPRESSURIZING_STATE, event)
            else:
                raise AssertionError("Unhandled case.")

    def _transition_to(self, state, event):
        if self._pre:
            if not self._pre(self, state, event):
                return
        self.state = state
        if self._post:
            self._post(self, state, event)
