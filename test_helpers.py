def namify(matrix, names):
    '''
    Walk through a 2D array; for any values that are integers, convert int to friendly name.
    '''
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            value = matrix[i][j]
            if type(value) == type(0):
                matrix[i][j] = names[value]
    return matrix

def check_transition(sm, event, trans, state_names, event_names):
    '''
    See if a particular event results in the expected transition, given a state machine
    in an initial state. If not, return a helpful error message about the discrepancy.
    '''
    start_state = state_names[sm.state]
    expected = trans if trans else state_names[sm.state]
    try:
        sm.handle(event)
        actual = state_names[sm.state]
    except Exception as ex:
        actual = 'ex'
    if actual != expected:
        return "%s + %s != %s -- new state = %s instead" % (start_state, event_names[event], expected, actual)
