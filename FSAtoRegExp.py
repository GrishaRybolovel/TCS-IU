class Edge:
    to = ""
    alpha = ""
    def __init__(self, to, s):
        self.to = to
        self.alpha = s
    def getAlpha(self):
        return self.alpha

    def getTo(self):
        return self.to


def e0(lines): #Input file is malformed
    cnt = 0
    for line in inp:
        line = line.strip(' ')
        cnt += 1
        if line == "" or line is None:
            return True
    if cnt != 5:
        return True

    if len(lines[0]) < 10 or len(lines[1]) < 8 or len(lines[2]) < 10 or len(lines[3]) < 12 or len(lines[4]) < 8:
        return True

    elif (lines[0][0:8] != "states=[") or (lines[0][-1] != "]") or (lines[1][0:7] != "alpha=[") or (lines[1][-1] != "]") or \
            (lines[2][0:9] != "initial=[") or (lines[2][-1] != "]") or (lines[3][0:11] != "accepting=[")\
            or (lines[3][-1] != "]") or (lines[4][0:7] != "trans=[") or (lines[4][-1] != "]"):
        return True

    return False

def fillStatesAndAlphabet(lines):
    global states
    global transitions
    global finite
    states = {}
    transitions = set()
    state = lines[0]
    counter = 1

    if len(lines[2]) == 0:
        fout.write("Error:\n" + "E4: Initial state is not defined")
        fout.close()
        return False

    for s in state:
        if s not in states and s != lines[2]:
            states[s] = counter
            counter += 1
        elif s == lines[2]:
            states[s] = 0

    if lines[2] not in states:
        fout.write("Error:\n" + "E1: A state '" + lines[2] + "' is not in the set of states")
        fout.close()
        return False

    alpha = lines[1]
    for element in alpha:
        transitions.add(element)
    finite = lines[3]

    for s in finite:
        if s not in states and len(s) > 0:
            fout.write("Error:\n" + "E1: A state '" + s + "' is not in the set of states")
            fout.close()
            return False
    return True

def getTransitions(lines):
    global graph
    trans = lines[4]
    dis = [False for i in range(len(states))]
    e3 = False
    t = ""
    for transition in trans:
        elements = transition.split('>')
        if elements[0] not in states:
            fout.write("Error:\n" + "E1: A state '" + elements[0] + "' is not in the set of states")
            fout.close()
            return False
        if elements[2] not in states:
            fout.write("Error:\n" + "E1: A state '" + elements[2] + "' is not in the set of states")
            fout.close()
            return False
        f = states[elements[0]]
        to = states[elements[2]]
        val = elements[1]
        if val not in transitions:
            e3 = True
            t = val
        h = Edge(to, val)
        graph[f].append(h)
        if f != to:
            dis[f] = True
            dis[to] = True
    if lines[2] not in states:
        fout.write("Error:\n" + "E3: A transition '" + lines[2] + "' is not represented in the alphabet")
        fout.close()
        return False

    if len(lines[2]) == 0:
        fout.write("Error:\n" + "E4: Initial state is not defined")
        fout.close()
        return False

    if len(states) > 1:
        for i in range(len(states)):
            if not dis[i]:
                fout.write("Error:\n" + "E2: Some states are disjoint")
                fout.close()
                return False
    if e3:
        fout.write("Error:\n" + "E3: A transition '" + t + "' is not represented in the alphabet")
        fout.close()
        return False
    return True

def e5():
    global graph
    for i in range(len(states)):
        trans = set()
        for e in graph[i]:
            if e.getAlpha() in trans:
                fout.write("Error:\n" + "E5: FSA is nondeterministic")
                fout.close()
                exit()
            trans.add(e.getAlpha())


def generate():
    ans = []
    n = len(states)
    for i in range(n + 1):
        r1 = []
        for j in range(n):
            r2 = []
            for k in range(n):
                r2.append("")
            r1.append(r2)
        ans.append(r1)

    for f in range(n):
        for t in range(n):
            s = ""
            for e in graph[f]:
                if e.getTo() == t:
                    if len(s) == 0:
                        s += e.getAlpha()
                    else:
                        s += "|" + e.getAlpha()
            if t == f:
                if len(s) == 0:
                    s += "eps"
                else:
                    s += "|eps"
            if len(s) == 0:
                s = "{}"
            ans[0][f][t] = "" + s
    for level in range(1, n + 1):
        for fr in range(n):
            for to in range(n):
                ans[level][fr][to] = "(" + ans[level - 1][fr][level - 1] + ")(" + ans[level - 1][level - 1][level - 1] + ")*(" + ans[level - 1][level - 1][to] + ")|(" + ans[level - 1][fr][to] + ")"
    writeAns(ans)


def writeAns(ans):
    answer = ""
    for s in finite:
        ind = states[s]
        if len(answer) == 0:
            answer += ans[len(states)][0][ind]
        else:
            answer += "|" + ans[len(states)][0][ind]
    fout.write(answer)
    fout.close()



if __name__ == "__main__":
    fin = open("input.txt", "r")
    fout = open("output.txt", "w")
    inp = fin.read().split('\n')
    cnt = 0
    newInp = []

    states = {}
    transitions = set()
    graph = []
    finite = []

    for line in inp:
        line = line.strip(' ')

    if e0(inp):
        fout.write("Error:\nE0: Input file is malformed")
        exit()

    for line in inp:
        if cnt == 0:
            newInp.append(line.split('=')[1][1:-1].split(','))

            cnt += 1
        elif cnt == 1:
            newInp.append(line.split('=')[1][1:-1].split(','))
            cnt += 1
        elif cnt == 2:
            newInp.append(line.split('=')[1][1:-1].split(',')[0])
            cnt += 1
        elif cnt == 3:
            newInp.append(line.split('=')[1][1:-1].split(','))
            cnt += 1
        elif cnt == 4:
            newInp.append(line.split('=')[1][1:-1].split(','))
            cnt += 1

    if not fillStatesAndAlphabet(newInp):
        exit()
    graph = [[] for i in range(len(states))]

    if not getTransitions(newInp):
        exit()
    e5()

    if len(finite) == 1 and finite[0] == "":
        fout.write("{}")
        fout.close()
        exit()
    generate()
