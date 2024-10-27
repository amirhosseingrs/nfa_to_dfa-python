#------------------------------- Declare variables ---------------------------------------------
# states = dict()
last_state = 10

# DTrans-Format : A:{"marked": False, "value": set(), "ecm_a": set(), "ecm_b": set(), "final": False}
DTrans = dict()

# states = {'q0':['1','7'],'q1':['2','4'],'q2':['a3'],'q3':['6'],'q4':['b5'],'q5':['6'],'q6':['1','7'],'q7':['a8'],'q8':[]}
states = {'q0':['1','3'],'q1':['a2'],'q2':['5'],'q3':['b4'],'q4':['5'],'q5':['6','8'],'q6':['a7'],'q7':['10'],'q8':['b9'], 'q9':['10'], 'q10': []}
DT_names = list('BCDEFGHIJKLMNOPQRSTUVWXYZ')
DT_names.reverse()







#------------------------------- Getting the States ---------------------------------------------
# for i in range(100) :
#     # Input Format : 1,a2,b3,4 
#     state = input(f'q{i}: ').split(",")

#     if 'end' in state :
#         last_state = len(states)
#         break

#     states[f'q{i}'] = state


#------------------------------- Declare Functions ---------------------------------------------
def ep(s):
    state = [int(x) for x in states[f'q{s}'] if 'a' not in x and 'b' not in x]
    # print(f'state for {s} = {state}')
    if len(state) == 0:
        return [s]

    new_states = []
    for i in state:
        new = ep(i)
        new_states.extend(new if isinstance(new, list) else [new])

    state.extend(new_states)
    state.append(int(s))
    return list(set(state))


def move(t,s):
    state = [x for x in states[f'q{t}'] if s in x]
    if len(state) > 0:
        state = state[0].replace(s,'')
    return state

def multy_move(ts,s):
    result = list()
    for i in ts:
        result = union(result, move(i,s))
    return result

def multy_ep(ts):
    result = list()
    for i in ts:
        result = union(result, ep(i))
    return result


def epc_move(ts,s):
    epc = multy_move(ts,s)
    epc = [int(x) for x in epc]
    epc = multy_ep(epc)
    return epc

def check_unmarkeds():
    for i in DTrans:
        marked = DTrans[i]['marked']
        if marked == False : 
            return i
    return False 
        
def add_DTrans(name, value, marked, ecm_a, ecm_b, final):
    DTrans[name] = {"marked": marked, "value": value, "ecm_a":ecm_a, "ecm_b": ecm_b,"final": final}    

def check_Dtrans(value):
    result = [key for key, info in DTrans.items() if info.get('value') == value]
    return result[0] if result else False

def union(a,b):
    for i in b:
        a.append(i)
    return a

#------------------------------- Start for Algorithm ---------------------------------------------
    # First Step : Finding epsilon_closure(First-State) -> DTrans['A']
ep_first = ep(0)
DTrans['A'] = {"marked": False, "value": ep_first, "final": False}    

    # Second Step : Marking DTrans
while(check_unmarkeds()):
    item = check_unmarkeds()
    value = DTrans[f'{item}']['value']


    ecm_a = epc_move(value, 'a')
    if check_Dtrans(ecm_a) == False:
        name = DT_names.pop()
        add_DTrans(name, ecm_a, False, set(), set(), last_state in ecm_a)
        DTrans[f'{item}']['ecm_a'] = name
    else: 
        DTrans[f'{item}']['ecm_a'] = check_Dtrans(ecm_a) 


    ecm_b = epc_move(value, 'b')
    if check_Dtrans(ecm_b) == False:
        name = DT_names.pop()
        add_DTrans(name, ecm_b, False, set(), set(), last_state in ecm_b)
        DTrans[f'{item}']['ecm_b'] = name
    else:
        DTrans[f'{item}']['ecm_b'] = check_Dtrans(ecm_b)

    DTrans[f'{item}']['marked'] = True

# print(DTrans)




#------------------------------- Output DFA ---------------------------------------------
for i in DTrans:
    it = i
    ecm_a = DTrans[f'{i}']['ecm_a']
    ecm_b = DTrans[f'{i}']['ecm_b']
    print(f'{it}---(a)--->{ecm_a}')
    print(f'{it}---(b)--->{ecm_b}')