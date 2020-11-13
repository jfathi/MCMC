from random import random, randint

COVID_BIT = 64
FEVER_BIT = 32
COUGH_BIT = 16
NAUSEA_BIT = 8
FEV_NAU_BIT = 4
FEV_COU_BIT = 2
COU_NAU_BIT = 1

TOTAL_VARS = 127
EVIDENCE_VARS = FEVER_BIT + FEV_NAU_BIT

def state_gen():
    state = randint(EVIDENCE_VARS,TOTAL_VARS)
    while (state & EVIDENCE_VARS != EVIDENCE_VARS):
        state = randint(EVIDENCE_VARS,TOTAL_VARS)
    return state

def flip_var(state,req_var):
    if (state & req_var != req_var):
        state += req_var
    else:
        state -= req_var
    return state


# SCRAPPED
# Note, for this to work, dictionaries MUST be ordered by probabilities.
def assign_condition(choices):
    
    val = random()

    n = len(choices)
    keys = choices.keys()

    if (n == 1):
        return keys[0]
    elif (n == 2):
        return keys[0] if (val < choices[keys[1]]) else keys[1]
    else:
        for x in range(n - 1):
            if (val >= choices[keys[x]]) and (val < choices[keys[x+1]]):
                return keys[x]
        return keys[n - 1]

def main():
    print('nothing yet')
    '''
    # 0. Initialize counters
    COVID_Counter = 0                   # t = 0
    Cough_Counter = Nausea_Counter = 0  # t = 1
    FevCou_Counter = CouNau_Counter = 0 # t = 2

    # 1. Generate bit representation of initial state
    start_state = state_gen()

    # 2. 
    '''
main()