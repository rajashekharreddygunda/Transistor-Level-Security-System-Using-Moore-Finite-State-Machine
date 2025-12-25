from quine_mccluskey.qm import QuineMcCluskey
qm = QuineMcCluskey()


machineType = int(input("Enter 0 for selecting Mealy machine or 1 for selecting Moore machine. "))
detectorType = int(input("Enter 0 for selecting overlapping or 1 for selecting non-overlapping. "))
flipflopType = int(input("Enter the flip flop type \n 0->D-flipflop \n 1->SR-flipflop \n 2->JK-flipflop \n 3->T-flipflop\n"))
sequence = input("Enter the sequence that has to be detected. ")

x = "x"  # dummy value for expressing don't care numerically


SR_execution_table = {"present": [0, 0, 1, 1], "next": [0, 1, 0, 1], "inputs": {"s": [0, 1, 0, x], "r": [x, 0, 1, 0]}}
D_execution_table = {"present": [0, 0, 1, 1], "next": [0, 1, 0, 1], "inputs": {"d": [0, 1, 0, 1]}}
JK_execution_table = {"present": [0, 0, 1, 1], "next": [0, 1, 0, 1], "inputs": {"j": [0, 1, x, x], "k": [x, x, 1, 0]}}
T_execution_table = {"present": [0, 0, 1, 1], "next": [0, 1, 0, 1], "inputs": {"t": [0, 1, 1, 0]}}


def create_state_diagram(seq: str, machine: int, detector: int) -> list[dict]:
    """
    generates and returns state diagram for the patterns detection of the given pattern
    :param seq: Input pattern that has to be detected
    :param machine: Type of machine mealy/ moore. 0 for mealy and 1 for moore
    :param detector: Type of pattern detection. 0 for overlapping and 1 for non overlapping
    :return: a list of states and transitions
    """
    result = []
    for i in range(len(seq)):  # to create a list of dictionaries
        result.append({})
    if machine:  # length of pattern + 1 states required for moore model
        result.append({})

    if machine:  # for moore machine
        for i in range(len(seq)):
            result[i]["output"] = 0  # output of all states except final state is 0
            result[i]["input " + seq[i]] = i + 1  # forwarding to final state for the given sequence
        result[-1]["output"] = 1  # output of the final state is 1

        if seq[0] == "0":  # wrong pattern detected in first state transitions to itself
            result[0]["input 1"] = 0
        else:
            result[0]["input 0"] = 0

        for i in range(1, len(seq)):  # pattern detection for in between states
            temp = "input "
            temp1 = seq[0:i]
            if seq[i] == "0":
                temp = temp + "1"
                temp1 = temp1 + "1"

            else:
                temp = temp + "0"
                temp1 = temp1 + "0"
            dummy = i
            output = i
            while dummy != 0:  # sliding window kind of thingy explained in clearly in documentation
                if seq[0:dummy] == temp1[-dummy:]:
                    output = dummy
                    break
                dummy = dummy-1
            if dummy == 0:
                output = 0
            result[i][temp] = output

        if detector:  # checking for overlapping sequence detector or non overlapping sequence detector
            if seq[0] == "0":
                result[-1]["input 0"] = 1
                result[-1]["input 1"] = 0
            else:
                result[-1]["input 0"] = 0
                result[-1]["input 1"] = 1
        else:
            i = len(seq)
            dummy = i
            temp1 = seq[1:] + "1"
            output = 0
            while dummy != 0:
                if seq[0:dummy] == temp1[-dummy:]:
                    output = dummy
                    break
                dummy = dummy - 1
            if dummy == 0:
                output = 0
            result[-1]["input 1"] = output

            dummy = i
            temp1 = seq[1:] + "0"
            output = 0
            while dummy != 0:
                if seq[0:dummy] == temp1[-dummy:]:
                    output = dummy
                    break
                dummy = dummy - 1
            if dummy == 0:
                output = 0
            result[-1]["input 0"] = output

    else:  # for mealy machine
        for i in range(len(seq)):
            result[i]["0"] = {}
            result[i]["1"] = {}

        if seq[0] == "0":
            temp = "1"
        else:
            temp = "0"
        result[0][temp]["next"] = 0
        result[0][temp]["output"] = 0
        result[0][seq[0]]["next"] = 1
        result[0][seq[0]]["output"] = 0

        for i in range(1, len(seq)-1):
            result[i][seq[i]]["next"] = i+1  # proceeding to next state on matched input
            result[i][seq[i]]["output"] = 0

            temp1 = seq[0:i]
            if seq[i] == "0":
                temp = "1"
                temp1 = temp1 + "1"

            else:
                temp = "0"
                temp1 = temp1 + "0"
            dummy = i
            output = i
            while dummy != 0:  # sliding window again
                if seq[0:dummy] == temp1[-dummy:]:
                    output = dummy
                    break
                dummy = dummy - 1
            if dummy == 0:
                output = 0
            result[i][temp]["next"] = output
            result[i][temp]["output"] = 0

        if detector:  # checking if the pattern detector is overlapping or non overlapping
            if seq[-1] == "0":
                temp = "0"
                nottemp = "1"
            else:
                temp = "1"
                nottemp = "0"
            result[-1][temp]["next"] = 0
            result[-1][temp]["output"] = 1
            result[-1][nottemp]["output"] = 0

            i = len(seq)
            dummy = i
            temp1 = seq[0:-1] + nottemp
            output = 0
            while dummy != 0:
                if seq[0:dummy] == temp1[-dummy:]:
                    output = dummy
                    break
                dummy = dummy - 1
            if dummy == 0:
                output = 0
            result[-1][nottemp]["next"] = output
        else:
            if seq[-1] == "0":
                temp = "0"
                nottemp = "1"
            else:
                temp = "1"
                nottemp = "0"
            result[-1][temp]["output"] = 1
            result[-1][nottemp]["output"] = 0

            i = len(seq)
            dummy = i
            temp1 = seq[0:-1] + nottemp
            output = 0
            while dummy != 0:
                if seq[0:dummy] == temp1[-dummy:]:
                    output = dummy
                    break
                dummy = dummy - 1
            if dummy == 0:
                output = 0
            result[-1][nottemp]["next"] = output

            i = len(seq)
            dummy = i-1
            temp1 = seq[:-1] + temp
            output = 0
            while dummy != 0:
                if seq[0:dummy] == temp1[-dummy:]:
                    output = dummy
                    break
                dummy = dummy - 1
            if dummy == 0:
                output = 0
            result[-1][temp]["next"] = output
    return result


def construct_transition_table(state_diagram: list[dict], flipflop: int) -> dict:
    transition_table = {}
    size = len(state_diagram)
    no_of_flip_flops = 0
    while size > 2**no_of_flip_flops:
        no_of_flip_flops = no_of_flip_flops + 1

    transition_table["present"] = []
    transition_table["input"] = []
    transition_table["next"] = []
    transition_table["output"] = []
    transition_table["flip flop input"] = {}
    if flipflop == 0:
        transition_table["flip flop input"]["d"] = []
    elif flipflop == 1:
        transition_table["flip flop input"]["s"] = []
        transition_table["flip flop input"]["r"] = []
    elif flipflop == 2:
        transition_table["flip flop input"]["j"] = []
        transition_table["flip flop input"]["k"] = []
    elif flipflop == 3:
        transition_table["flip flop input"]["t"] = []
    for i in range(size):
        temp = bin(i)[2:]

        while len(temp) < no_of_flip_flops:
            temp = "0"+temp

        transition_table["present"].append(temp[-no_of_flip_flops:])  # appending present states to the transition table
        transition_table["present"].append(temp[-no_of_flip_flops:])
        transition_table["input"].append("0")  # appending inputs to the transition table
        transition_table["input"].append("1")

        if machineType:
            temp1 = bin(state_diagram[i]["input 0"])[2:]
            temp2 = bin(state_diagram[i]["input 1"])[2:]
            transition_table["output"].append(bin(state_diagram[i]["output"])[2:])
            transition_table["output"].append(bin(state_diagram[i]["output"])[2:])

        else:
            temp1 = bin(state_diagram[i]["0"]["next"])[2:]
            temp2 = bin(state_diagram[i]["1"]["next"])[2:]
            op1 = bin(state_diagram[i]["0"]["output"])
            op2 = bin(state_diagram[i]["1"]["output"])
            transition_table["output"].append(op1[2:])
            transition_table["output"].append(op2[2:])

        while len(temp1) < no_of_flip_flops:
            temp1 = "0" + temp1

        while len(temp2) < no_of_flip_flops:
            temp2 = "0" + temp2

        transition_table["next"].append(temp1)
        transition_table["next"].append(temp2)

    for i in range(2*size):
        if flipflop == 0:
            res = ""
            for j in range(no_of_flip_flops):
                present = transition_table["present"][i][j]
                nxt = transition_table["next"][i][j]
                for k in range(4):
                    if present == bin(D_execution_table["present"][k])[2:] and nxt == bin(D_execution_table["next"][k])[2:]:
                        res = res+bin(D_execution_table["inputs"]["d"][k])[2:]
                        break
            transition_table["flip flop input"]["d"].append(res)

        elif flipflop == 1:
            res1 = ""
            res2 = ""
            for j in range(no_of_flip_flops):
                present = transition_table["present"][i][j]
                nxt = transition_table["next"][i][j]
                for k in range(4):
                    if present == bin(SR_execution_table["present"][k])[2:] and nxt == bin(
                            SR_execution_table["next"][k])[2:]:
                        if SR_execution_table["inputs"]["s"][k] == "x":
                            res1 = res1 + "x"
                        else:
                            res1 = res1 + bin(SR_execution_table["inputs"]["s"][k])[2:]

                        if SR_execution_table["inputs"]["r"][k] == "x":
                            res2 = res2 + "x"
                        else:
                            res2 = res2 + bin(SR_execution_table["inputs"]["r"][k])[2:]

                        break
            transition_table["flip flop input"]["s"].append(res1)
            transition_table["flip flop input"]["r"].append(res2)

        elif flipflop == 2:
            res1 = ""
            res2 = ""
            for j in range(no_of_flip_flops):
                present = transition_table["present"][i][j]
                nxt = transition_table["next"][i][j]
                for k in range(4):
                    if present == bin(JK_execution_table["present"][k])[2:] and nxt == bin(JK_execution_table["next"][k])[2:]:
                        if JK_execution_table["inputs"]["j"][k] == "x":
                            res1 = res1+"x"
                        else:
                            res1 = res1 + bin(JK_execution_table["inputs"]["j"][k])[2:]

                        if JK_execution_table["inputs"]["k"][k] == "x":
                            res2 = res2+"x"
                        else:
                            res2 = res2 + bin(JK_execution_table["inputs"]["k"][k])[2:]

                        break
            transition_table["flip flop input"]["j"].append(res1)
            transition_table["flip flop input"]["k"].append(res2)

        elif flipflop == 3:
            res = ""
            for j in range(no_of_flip_flops):
                present = transition_table["present"][i][j]
                nxt = transition_table["next"][i][j]
                print(present)
                print(nxt)
                print("fuck")
                for k in range(4):
                    if present == bin(T_execution_table["present"][k])[2:] and nxt == bin(T_execution_table["next"][k])[2:]:
                        res = res + bin(T_execution_table["inputs"]["t"][k])[2:]
                        break
            transition_table["flip flop input"]["t"].append(res)

    return transition_table


def term_to_expr(term, vars):
    expr = []
    for bit, var in zip(term, vars):
        if bit == '1':
            expr.append(var)
        elif bit == '0':
            expr.append(var + "'")
    return ''.join(expr)


def driving_expression_generator(transition_table: dict, flipflop: int):
    print(transition_table)
    mins = []
    dont_cares = []
    size = len(transition_table["output"])
    no_of_flip_flops = 0

    while size > 2 ** no_of_flip_flops:
        no_of_flip_flops = no_of_flip_flops + 1

    if flipflop == 0:
        for i in range(no_of_flip_flops-1):
            mins.append([])
            dont_cares.append([])
            for j in range(size):
                if transition_table["flip flop input"]["d"][j][i] == "1":
                    mins[i].append(j)
                elif transition_table["flip flop input"]["d"][j][i] == "x":
                    dont_cares[i].append(j)
            for j in range(size, 2**no_of_flip_flops):
                dont_cares[i].append(j)

    elif flipflop == 1:
        for i in range(2 * (no_of_flip_flops - 1)):
            mins.append([])
            dont_cares.append([])

        for i in range(no_of_flip_flops - 1):
            for j in range(size):
                if transition_table["flip flop input"]["s"][j][i] == "1":
                    mins[i].append(j)
                elif transition_table["flip flop input"]["s"][j][i] == "x":
                    dont_cares[i].append(j)

            for j in range(size, 2 ** no_of_flip_flops):
                dont_cares[i].append(j)

            for j in range(size):
                if transition_table["flip flop input"]["r"][j][i] == "1":
                    mins[no_of_flip_flops + i - 1].append(j)
                elif transition_table["flip flop input"]["r"][j][i] == "x":
                    dont_cares[no_of_flip_flops + i - 1].append(j)

            for j in range(size, 2 ** no_of_flip_flops):
                dont_cares[no_of_flip_flops + i - 1].append(j)

    elif flipflop == 2:
        for i in range(2 * (no_of_flip_flops - 1)):
            mins.append([])
            dont_cares.append([])

        for i in range(no_of_flip_flops - 1):
            for j in range(size):
                if transition_table["flip flop input"]["j"][j][i] == "1":
                    mins[i].append(j)
                elif transition_table["flip flop input"]["j"][j][i] == "x":
                    dont_cares[i].append(j)

            for j in range(size, 2 ** no_of_flip_flops):
                dont_cares[i].append(j)

            for j in range(size):
                if transition_table["flip flop input"]["k"][j][i] == "1":
                    mins[no_of_flip_flops+i-1].append(j)
                elif transition_table["flip flop input"]["k"][j][i] == "x":
                    dont_cares[no_of_flip_flops+i-1].append(j)

            for j in range(size, 2 ** no_of_flip_flops):
                dont_cares[no_of_flip_flops+i-1].append(j)

    elif flipflop == 3:
        for i in range(no_of_flip_flops - 1):
            mins.append([])
            dont_cares.append([])
            for j in range(size):
                if transition_table["flip flop input"]["t"][j][i] == "1":
                    mins[i].append(j)
                elif transition_table["flip flop input"]["t"][j][i] == "x":
                    dont_cares[i].append(j)
            for j in range(size, 2 ** no_of_flip_flops):
                dont_cares[i].append(j)

    mins.append([])
    dont_cares.append([])
    for i in range(size):
        if transition_table["output"][i] == "1":
            mins[-1].append(i)
        elif transition_table["output"][i] == "x":
            dont_cares[-1].append(i)

    for i in range(size, 2**no_of_flip_flops):
        dont_cares[-1].append(i)

    dummies = []

    for i in range(no_of_flip_flops-2, -1, -1):
        temp = "Q"+str(i)
        dummies.append(temp)
    dummies.append("X")
    for i in range(len(mins)):
        result = qm.simplify(mins[i], dont_cares[i], no_of_flip_flops)
        for j in result:
            print(term_to_expr(j, dummies), end=" + ")
        print("")








temporary = create_state_diagram(sequence, machineType, detectorType)
trans = construct_transition_table(temporary, flipflopType)
driving_expression_generator(trans, flipflopType)