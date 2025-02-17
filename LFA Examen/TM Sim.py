# Membrii echipei : Rada Paul , Bicu Radu Florian
import re

def transform():
    global stare,Head,Tape1,prev,stop

    prev = Tape1[Head]

    if Transitions[stare].get([Tape1[Head]][0]) is None:                #daca nu exista cheia
        stop=1
        return

    Tape1[Head]=Transitions[stare][Tape1[Head]][0]

    if Transitions[stare][prev][1]=='R':
        Head+=1
    else:
        Head-=1
    stare=Transitions[stare][prev][2]


def Valid():
    for letter in Sigma:
        if letter not in Alphabet:
            return 0
    if len(States_s) > 1 or len(States_f) > 1:
        return 0
    for state in Transitions.keys():
        if state not in States:
            return 0
        for key in Transitions[state]:
            if key not in Alphabet:
                return 0
        for elements in Transitions[state].values():
            if elements[0] not in Alphabet or elements[2] not in States:
                return 0
            if elements[1] != 'R' and elements[1] != "L":
                return 0
    if Tape1!=Tape2:                                    #check for the integrity of the tapes (if they are identical).(ex4)
        return 0                                        #de asemenea exercitiul 3
            
    return 1

Sigma = []
Alphabet = []
States = []
Transitions = {}
States_s = []
States_f = []
Head=None
Tape1=[]
Tape2=[]                #backup copy

with open("tm_config_file.txt") as f:
    while True:
        s = f.readline()
        s = s.rstrip()
        if s == "":
            break
        if s == "Sigma:":
            s = f.readline()
            s = s.rstrip()
            while s != "End":
                Sigma.append(s)
                s = f.readline()
                s = s.rstrip()
        if s == "Alphabet:":
            s = f.readline()
            s = s.rstrip()
            while s != "End":
                Alphabet.append(s)
                s = f.readline()
                s = s.rstrip()
        if s == "States:":
            s = f.readline()
            s = s.rstrip()
            while s != "End":
                s = s.split(" ")
                if len(s) > 1:
                    if s[1] == "S":
                        States_s.append(s[0])
                    if s[1] == "F":
                        States_f.append(s[0])
                States.append(s[0])
                s = f.readline()
                s = s.rstrip()
        if s == "Transitions:":
            s = f.readline()
            s = s.rstrip()
            while s != "End":
                elements = re.compile(r" |: |->").split(s)
                if elements[0] not in Transitions:
                    Transitions[elements[0]] = {}
                Transitions[elements[0]][elements[2]] = [elements[3], elements[4], elements[1]]
                s = f.readline()
                s = s.rstrip()

        if s == "Head:":
            s = f.readline()
            s = s.rstrip()
            while s != "End":
                Head=int(s[0])
                s = f.readline()
                s = s.rstrip()

        if s == "Tape1:":
            s = f.readline()
            s = s.rstrip()
            while s != "End":
                Tape1.append(s)
                s = f.readline()
                s = s.rstrip()

        if s == "Tape2:":
            s = f.readline()
            s = s.rstrip()
            while s != "End":
                Tape2.append(s)
                s = f.readline()
                s = s.rstrip()
    
if Valid() == 1:
    print("Configuration is valid")
else:
    print("Configuration is not valid")

if Valid() == 1:
    stare = 'q1'
    prev=0
    stop=0

    while(True):
        transform()
        if stop==1:
            print("Input is not valid")
            break
        if stare=='q8':
            if Transitions[stare].get([Tape1[Head]][0]) is None:
                print("Input is not valid")
                break
            if Transitions[stare][Tape1[Head]][0]=='_':
                print("Input is valid")
                break
