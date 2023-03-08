sgm = 0 # nu suntem la citirea din sigma
sts = 0 # nu suntem la citirea din states
trs = 0
dfa_valid = 1 #presupunem ca DFA valid
si = -1 #pentru a observa dfa valid
stari_initiale = 0
nr_states = 0
sigma = []
states = []
final_states = []
f = open("dfa_config_file.txt", 'r')
for line in f.readlines():
    if line[0]  == "#":
        continue
    if sgm == 1:
        sigma.append(line[0])
    if "Sigma" in line:
        sgm = 1 # am citit sigma
    if sgm == 1 and "End" in line: # am terminat citirea cu sigma
        sgm = 0
    if "End" in line and sts == 1:
        sts = 0
        ma = [[0 for i in range(nr_states+1)] for j in range(nr_states+1)]
    if sts == 1:
        nr_states += 1
        line = line.replace(', ','')
        states.append(int(line[0]))
        if 'S' in line:
            stari_initiale += 1
            si = int(line[0]) 
            if stari_initiale != 1:
                dfa_valid = 0
        if 'F' in line:
            final_states.append(int(line[0]))
    if "States" in line:
        sts = 1
    if "End" in line and trs == 1:
        trs = 0
    if trs == 1:
        line =  line.replace(', ','')
        state1 = int(line[0])
        letter = line[1]
        state2 = int(line[2])
        if letter not in sigma:
            dfa_valid = 0
        if ma[state1][state2] != 0:
            dfa_valid = 0
        ma[state1][state2] = letter
    if "Transitions" in line:
        trs = 1

if dfa_valid == 0:
    print("DFA INVALID!!!")
else:
    print("DFA VALID!!!")