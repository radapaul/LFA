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


def read_state(lines,initial_states):
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


def read_transition(lines,transitions_letters):
    transitions = {}
    del lines[0]
    line = lines[0]

    while "End" not in line:
        line = line.replace(", ", "")
        aux = [line[1], line[2]]
        transitions_letters.append(line[1])

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
    transitions_letters=[]
    check_transitions_letters=1
    initial_states=0

    while len(lines) > 0:
        line = lines[0]
        if line.startswith("#"):
            del lines[0]
            continue
        if "States" in line:
            states = read_state(lines,initial_states)
            continue
        if "Transitions" in line:
            transitions = read_transition(lines,transitions_letters)
            continue
        if "Sigma" in line:
            alphabet = read_alphabet(lines)
            continue

    for i in range(len(transitions_letters)):
        if transitions_letters[i] not in alphabet:
            check_transitions_letters=0

    if len(states[0])!=1 or check_transitions_letters == 0:
        print("NFA invalid")
    else:
        print("NFA valid")

if __name__ == "__main__":
    main()
