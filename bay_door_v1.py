# Define states and events, including symbolic (numeric) constants and their friendly names.
STATE_NAMES = ['open', 'closed', 'opening', 'closing']
for i in range(len(STATE_NAMES)):
    globals()[STATE_NAMES[i].upper() + '_STATE'] = i
EVENT_NAMES = ['open requested', 'close requested', 'finished opening', 'finished closing']
for i in range(len(EVENT_NAMES)):
    globals()[EVENT_NAMES[i].upper().replace(' ', '_') + '_EVENT'] = i

class StateMachine:

    def __init__(self):
        self.state = CLOSED_STATE

    def handle(self, event):
        s = self.state
        if event == OPEN_REQUESTED_EVENT:
            if s in [CLOSED_STATE, CLOSING_STATE]:
                self.transition_to(OPENING_STATE)
        elif event == CLOSE_REQUESTED_EVENT:
            if s in [OPEN_STATE, OPENING_STATE]:
                self.transition_to(CLOSING_STATE)
        elif event == FINISHED_OPENING_EVENT:
            if s == OPENING_STATE:
                self.transition_to(OPEN_STATE)
            else:
                illegal = True
                raise AssertionError("Illegal event %s for state %s." % (EVENT_NAMES[event], STATE_NAMES[s]))
        elif event == FINISHED_CLOSING_EVENT:
            if s == CLOSING_STATE:
                self.transition_to(CLOSED_STATE)
            else:
                raise AssertionError("Illegal event %s for state %s." % (EVENT_NAMES[event], STATE_NAMES[s]))
        else:
            raise AssertionError("Illegal event %d." % event) #programmer error

    def transition_to(self, state):
        self.state = state
