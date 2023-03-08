def read_alphabet(lines):
    alphabet = []
    del lines[0]
    line = lines[0]
    while "End" not in line:
        alphabet.append(line[0])
        del lines[0]
        line = lines[0]

    del lines[0]
    return alphabet


def read_state(lines, nr_states):
    states = [[], [], []]
    nr_states = 0;
    del lines[0]
    line = lines[0]
    while "End" not in line:
        nr_states += 1
        line = line.replace(", ", "")
        if "S" in line:
            states[0].append(line[0])
        if "F" in line:
            states[1].append(line[0])
        if "F" not in line and "S" not in line:
            states[2].append(line[0])

        del lines[0]
        line = lines[0]

    del lines[0]
    return states


def read_transition(lines):
    transitions = []
    del lines[0]
    line = lines[0]

    while "End" not in line:
        line = line.replace(", ", "")
        aux = [line[0], line[1], line[2]]
        transitions.append(aux)

        del lines[0]
        line = lines[0]

    del lines[0]
    return transitions

def key_list(list):
    string=""
    for i in range(len(list)):
        string += str(list[i])
        string+=","
    string = string.strip(",")
    return string


def main():
    filename = "nfa_config_file.txt"
    f = open(filename, 'r')
    lines = f.readlines()
    nr_states = 0
    states = []
    alphabet = []
    transitions = {}

    while len(lines) > 0:
        line = lines[0]
        if line.startswith("#"):
            del lines[0]
            continue
        if "States" in line:
            states = read_state(lines, nr_states)
            continue
        if "Transitions" in line:
            transitions = read_transition(lines)
            continue
        if "Sigma" in line:
            alphabet = read_alphabet(lines)
            continue

    max1 = max(states[0])
    max2 = max(states[1])
    max3 = max(states[2])
    nr_states = int(max(max1, max2, max3))

    ma = [[0 for i in range(nr_states+1)] for j in range(nr_states+1)]

    #marcam pentru prima data matricea
    for i in range(nr_states+1):
        for j in range(i):
            if( ((str(i) in states[1]) and (str(j) not in states[1])) or ((str(i) not in states[1]) and (str(j) in states[1]))):
                ma[i][j] = 1

    marcari = 1
    while marcari:
        marcari = 0
        for i in range(nr_states+1):
            for j in range(i):
                if ma[i][j] == 0:
                    gasit = 0
                    for letter in alphabet:
                        i1 = ''
                        j1 = ''
                        if gasit==1:
                            break
                        for trans in transitions:
                            if trans[0]==str(i) and trans[1]==letter:
                                i1 = trans[2]
                            if trans[0]==str(j) and trans[1]==letter:
                                j1=trans[2]
                        if i1!='' and j1!='':
                            if ma[int(i1)][int(j1)]==1:
                                gasit=1
                                ma[i][j]=1
                                marcari+=1

    empty=[]
    for i in range(nr_states+1):
            for j in range(i):
                if ma[i][j]==0:
                    empty.append((i, j))


    #lista de seturi
    lista_seturi = []
    for pereche_stari in empty:
        ok = 0
        for stari in lista_seturi:
            if pereche_stari[0] in stari or pereche_stari[1] in stari:
                stari.add(pereche_stari[0])
                stari.add(pereche_stari[1])
                ok = 1
                break
        if ok == 0:
            lista_seturi.append({pereche_stari[0], pereche_stari[1]})

    #verificam daca din starile initiale gasim in lista de seturi, daca nu, adaugam starea

    for x in states:
        for y in x:
            ok = 1
            for stari in lista_seturi:
                if int(y) in stari:
                    ok = 0
            if ok == 1:
                lista_seturi.append({int(y)})
    new_states=[]
    for i in range(len(lista_seturi)):
        new_states.append(list(lista_seturi[i]))

    d = {}
    for x in lista_seturi:
        tup = tuple(x)
        d[tup] = []
        for letter in alphabet:
            letter_list = [] # retinem in ce stari au tranzitii elementele din setul curent pe litera curenta
            for state in x:
                for trans in transitions:
                    if trans[0] == state and trans[1] == letter:
                        letter_list.append(trans[2])

    final=[]
    for i in range(len(lista_seturi)):
        s=list(lista_seturi[i])
        final.append(s)

    for x in final:  #noduri finale
        key= tuple(x)
        for a in x:  #verific noduri initiale din nod combinat
            for b in range(len(transitions)):  #parcurg tranzitii initiale
                if int(transitions[b][0]) == a:  # daca vreun nod din cele combinate se duce in el insusi
                    if int(transitions[b][2]) in x:
                        aux=[transitions[b][1],tuple(x)]
                        d[key].append(aux)
                    if int(transitions[b][2]) not in x:
                        for nod in final:
                            if int(transitions[b][2]) in nod:
                                aux = [transitions[b][1],tuple(nod)]
                                d[key].append(aux)

    for x in d:
        for i in range(len(d[x])):
            j=i+1
            while j < len(d[x]):
                if(d[x][i]==d[x][j]):
                    del d[x][j]
                    j-=1
                j+=1

    new_d={}
    count=-1
    for key in d:
        count+=1
        for j in d:
            for i in range(len(d[j])):
                if d[j][i][1] == tuple(new_states[count]):
                    d[j][i][1]=count

    i=0
    for key in d:
        new_d[i]=[]
        new_d[i]=d[key]
        i+=1

    f = open("output","w")
    f.write("Sigma:")
    f.write('\n')
    for i in range(len(alphabet)):
        f.write(alphabet[i])
        f.write('\n')
    f.write("End")
    f.write('\n')

    f.write("States:")
    f.write('\n')
    count=-1
    for key,value in d.items():
        count+=1
        for i in range(len(key)):
            if str(key[i]) in states[0]:
                f.write(str(count))
                f.write(", S")
                f.write('\n')
                break
            if str(key[i]) in states[1]:
                f.write(str(count))
                f.write(", F")
                f.write('\n')
                break
            if str(key[i]) in states[2]:
                f.write(str(count))
                f.write('\n')
                break
    f.write("End")
    f.write('\n')

    f.write("Transitions:")
    f.write('\n')
    for key,value in new_d.items():
        for i in range(len(new_d[key])):
            f.write(str(key))
            for j in range(len(new_d[key][i])):
                f.write(', ')
                f.write(str(new_d[key][i][j]))
            f.write('\n')
    f.write("End")

if __name__ == "__main__":
    main()
