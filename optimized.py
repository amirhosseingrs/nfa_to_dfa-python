# Declare variables
last_state = 10
DTrans = dict()

states = {
    'q0': ['1', '3'], 'q1': ['a2'], 'q2': ['5'], 'q3': ['b4'], 'q4': ['5'],
    'q5': ['6', '8'], 'q6': ['a7'], 'q7': ['10'], 'q8': ['b9'], 'q9': ['10'], 'q10': []
}
DT_names = list('BCDEFGHIJKLMNOPQRSTUVWXYZ')[::-1]

# Declare Functions
def ep(s):
    state = {int(x) for x in states[f'q{s}'] if 'a' not in x and 'b' not in x}
    if not state:
        return {s}
    for i in list(state):
        state.update(ep(i))
    state.add(int(s))
    return state

def move(t, s):
    state = [x for x in states[f'q{t}'] if s in x]
    return state[0].replace(s, '') if state else ''

def multy_move(ts, s):
    result = set()
    for i in ts:
        result.update(move(i, s))
    return result

def multy_ep(ts):
    result = set()
    for i in ts:
        result.update(ep(i))
    return result

def epc_move(ts, s):
    epc = multy_move(ts, s)
    return multy_ep(int(x) for x in epc)

def check_unmarkeds():
    return next((i for i, info in DTrans.items() if not info['marked']), None)

def add_DTrans(name, value, marked, ecm_a, ecm_b, final):
    DTrans[name] = {"marked": marked, "value": value, "ecm_a": ecm_a, "ecm_b": ecm_b, "final": final}

def check_Dtrans(value):
    return next((key for key, info in DTrans.items() if info['value'] == value), None)

# Union function to combine sets
def union(a, b):
    return a | b

# Start Algorithm
# First Step: Finding epsilon_closure(First-State) -> DTrans['A']
ep_first = ep(0)
add_DTrans('A', ep_first, False, set(), set(), last_state in ep_first)

# Second Step: Marking DTrans
while unmarked := check_unmarkeds():
    value = DTrans[unmarked]['value']

    # Compute ecm_a
    ecm_a = epc_move(value, 'a')
    if not (name := check_Dtrans(ecm_a)):
        name = DT_names.pop()
        add_DTrans(name, ecm_a, False, set(), set(), last_state in ecm_a)
    DTrans[unmarked]['ecm_a'] = name

    # Compute ecm_b
    ecm_b = epc_move(value, 'b')
    if not (name := check_Dtrans(ecm_b)):
        name = DT_names.pop()
        add_DTrans(name, ecm_b, False, set(), set(), last_state in ecm_b)
    DTrans[unmarked]['ecm_b'] = name

    DTrans[unmarked]['marked'] = True

# Output DFA
for i in DTrans:
    ecm_a = DTrans[i]['ecm_a']
    ecm_b = DTrans[i]['ecm_b']
    print(f"{i}---(a)--->{ecm_a}")
    print(f"{i}---(b)--->{ecm_b}")
