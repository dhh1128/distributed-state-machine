# Define states and events, including symbolic (numeric) constants and their friendly names.
STATE_NAMES = ['open', 'closed', 'opening', 'closing']
for i in range(len(STATE_NAMES)):
    globals()[STATE_NAMES[i].upper() + '_STATE'] = i
EVENT_NAMES = ['open requested', 'close requested', 'finished opening', 'finished closing']
for i in range(len(EVENT_NAMES)):
    globals()[EVENT_NAMES[i].upper().replace(' ', '_') + '_EVENT'] = i

class StateMachine:

    def __init__(self, pre=None, post=None):
        self.state = CLOSED_STATE
        self.pre = pre
        self.post = post

    def handle(self, event):
        s = self.state
        if event == OPEN_REQUESTED_EVENT:
            if s in [CLOSED_STATE, CLOSING_STATE]:
                self._transition_to(OPENING_STATE, event)
        elif event == CLOSE_REQUESTED_EVENT:
            if s in [OPEN_STATE, OPENING_STATE]:
                self._transition_to(CLOSING_STATE, event)
        elif event == FINISHED_OPENING_EVENT:
            if s == OPENING_STATE:
                self._transition_to(OPEN_STATE, event)
            else:
                illegal = True
                raise AssertionError("Illegal event %s for state %s." % (EVENT_NAMES[event], STATE_NAMES[s]))
        elif event == FINISHED_CLOSING_EVENT:
            if s == CLOSING_STATE:
                self._transition_to(CLOSED_STATE, event)
            else:
                raise AssertionError("Illegal event %s for state %s." % (EVENT_NAMES[event], STATE_NAMES[s]))
        else:
            raise AssertionError("Illegal event %d." % event) #programmer error

    def _transition_to(self, state, event):
        if self.pre:
            if not self.pre(self, state, event):
                return
        self.state = state
        if self.post:
            self.post(self, state, event)
