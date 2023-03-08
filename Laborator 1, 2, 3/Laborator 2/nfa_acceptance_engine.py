def check_validity(alphabet, states, transitions, word,start):
    if len(word)==0:
        return 0
    for letter in word:
        if letter not in alphabet:
            return 0
    cuv = word
    for letter in cuv:
        for i in range(len(transitions[start])):
            if letter in transitions[start][i]:
                current = transitions[start][i][1]
                if len(cuv) == 1 and transitions[start][i][1] in states[1]:
                    return 1
                word = cuv[1:]
                return check_validity(alphabet, states, transitions, word, current)
    return 0


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


def read_state(lines):
    states = [[], [], []]
    del lines[0]
    line = lines[0]
    while "End" not in line:
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
    transitions = {}
    del lines[0]
    line = lines[0]

    while "End" not in line:
        line = line.replace(", ", "")
        aux = [line[1], line[2]]

        if line[0] not in transitions:
            transitions[line[0]] = []
            transitions[line[0]].append(aux)
        else:
            transitions[line[0]].append(aux)

        del lines[0]
        line = lines[0]

    del lines[0]
    return transitions


def main():
    filename = "nfa_config_file.txt"
    f = open(filename, 'r')
    lines = f.readlines()
    states = []
    alphabet = []
    transitions = {}

    while len(lines) > 0:
        line = lines[0]
        if line.startswith("#"):
            del lines[0]
            continue
        if "States" in line:
            states = read_state(lines)
            continue
        if "Transitions" in line:
            transitions = read_transition(lines)
            continue
        if "Sigma" in line:
            alphabet = read_alphabet(lines)
            continue

    start = states[0][0]

    word = input("Input word:")
    ok = check_validity(alphabet, states, transitions, word,start)
    if ok == 1:
        print("AFN Valid")
    else:
        print("AFN Invalid")

if __name__ == "__main__":
    main()
