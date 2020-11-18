from csv import reader
from random import random, randint

Probabilties = []
StatesVisited = {}
TransitTable = {}

COVID_BIT = 64
FEVER_BIT = 32
COUGH_BIT = 16
NAUSEA_BIT = 8
FEV_COU_BIT = 4
FEV_NAU_BIT = 2
COU_NAU_BIT = 1

TOTAL_VARS = 127
EVIDENCE_VARS = NAUSEA_BIT + FEV_NAU_BIT

COVID_Counter = 0                                    # t = 0
Fever_Counter = Cough_Counter = Nausea_Counter = 0   # t = 1
FevNau_Counter = FevCou_Counter = CouNau_Counter = 0 # t = 2

PROBABILITY_FILE = 'Probability_Chart.csv'
COVID_COL = 2
FEVER_COL = 3
COUGH_COL = 4
NAUSEA_COL = 5
FEV_COU_COL = 6
FEV_NAU_COL = 7
COU_NAU_COL = 8

NUM_RUNS = 1
EXPERIMENTS_PER_RUN = 500000
VAL_CHECK = -1 # <- Edit this value to see how (COVID) counters changes during experiment.

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

def iterate_counters(state):
    
    if (state & COVID_BIT == COVID_BIT):
        global COVID_Counter
        COVID_Counter += 1

    if (state & FEVER_BIT == FEVER_BIT):
        global Fever_Counter
        Fever_Counter += 1
    
    if (state & COUGH_BIT == COUGH_BIT):
        global Cough_Counter
        Cough_Counter += 1
    
    if (state & NAUSEA_BIT == NAUSEA_BIT):
        global Nausea_Counter
        Nausea_Counter += 1
    
    if (state & FEV_NAU_BIT == FEV_NAU_BIT):
        global FevNau_Counter
        FevNau_Counter += 1
    
    if (state & FEV_COU_BIT == FEV_COU_BIT):
        global FevCou_Counter
        FevCou_Counter += 1
    
    if (state & COU_NAU_BIT == COU_NAU_BIT):
        global CouNau_Counter
        CouNau_Counter += 1


def probability_flip(state, variable_col, variable_val):
    
    true_var_prob = float(Probabilties[state - 1][variable_col])

    toss = random()    
    
    if ((toss <= true_var_prob) and (state & variable_val != variable_val))\
        or ((toss > true_var_prob) and (state & variable_val == variable_val)):
        state = flip_var(state, variable_val)
    
    return state

def main():

    global Probabilties, StatesVisited, TransitTable
    Probabilties = list(reader(open(PROBABILITY_FILE,"r")))

    makeTransitTable = input('Generate transition table? (Y/N) ').strip().upper()[0] == 'Y'
    
    print()

    init_state = state_gen()
    state = init_state
    num_experiments = NUM_RUNS * EXPERIMENTS_PER_RUN
    for i in range(1,num_experiments+1):
        
        prev_state = state
        
        # Comment out until the other probabilities are done!
        #if type(Probabilties[state - 1][0] == type('string')):
        #    Probabilties[state - 1] = [float(i) for i in Probabilties[state - 1]]

        # Remove when the other probabilities are done!
        if type(Probabilties[state - 1][0] == type('string')):
            for x in range(len(Probabilties[state - 1])):
                if x != FEVER_COL and x != COUGH_COL:
                    Probabilties[state - 1][x] = float(Probabilties[state - 1][x])

        iterate_counters(state)

        # Time, t = 0
        state = probability_flip(state, COVID_COL, COVID_BIT)
        
        # Time, t = 1
        # state = probability_flip(state, FEVER_COL, FEVER_BIT) | probability_flip(state, COUGH_COL, COUGH_BIT)
        #-----------------
        # state = probability_flip(state, FEVER_COL, FEVER_BIT)
        # state = probability_flip(state, COUGH_COL, COUGH_BIT)
        # state = probability_flip(state, NAUSEA_COL, NAUSEA_BIT)
        
        # Time, t = 2
        state = probability_flip(state, FEV_COU_COL, FEV_COU_BIT)
        state = probability_flip(state, COU_NAU_COL, COU_NAU_BIT)
        #state = probability_flip(state, FEV_COU_COL, FEV_COU_BIT)
        #state = probability_flip(state, COU_NAU_COL, COU_NAU_BIT)

        #print('{:b}'.format(state))

        if state not in StatesVisited:
            StatesVisited[state] = 0
        StatesVisited[state] += 1

        if makeTransitTable:
            transition = f'{prev_state:07b} -> {state:07b}'
            if transition not in TransitTable:
                TransitTable[transition] = 0
            TransitTable[transition] += 1

        if (i % VAL_CHECK == 0) and (VAL_CHECK > 0):
            print(f'Probability of COVID given Nausea, Fever&Nausea, i={i}: {COVID_Counter/i*100}%')

    print()

    if makeTransitTable:
        print('------------------')
        print('Transition Table')
        print('------------------')
        for transition in TransitTable:
            print(f'{transition} : {TransitTable[transition]}')
        print('------------------')
    
    if (input('Show state count table? (Y/N) ').strip().upper()[0] == 'Y'):
        print('------------------')
        print(f'Start: {init_state:07b}')
        print('------------------')
        print(' BitStr | Count')
        print('--------|---------')
        for key, value in StatesVisited.items():
            print(f"{key:07b}", ' | ', value, sep='')
        print('------------------')

    if (input('Show variable ratios? (Y/N) ').strip().upper()[0] == 'Y'):
        print(f'COVID:   {COVID_Counter/num_experiments}')
        print(f'FEVER:   {Fever_Counter/num_experiments}')
        print(f'COUGH:   {Cough_Counter/num_experiments}')
        print(f'NAUSEA:  {Nausea_Counter/num_experiments}')
        print(f'FEV+COU: {FevCou_Counter/num_experiments}')
        print(f'FEV+NAU: {FevNau_Counter/num_experiments}')
        print(f'FEV+COU: {CouNau_Counter/num_experiments}')

    print(f'\nProbability of COVID given Nausea, Fever&Nausea, i={i}: {COVID_Counter/i*100}%\n')

main()
