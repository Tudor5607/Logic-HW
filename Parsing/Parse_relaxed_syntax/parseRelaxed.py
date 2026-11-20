atomic_propositions = [f(x) for x in range(65,91) for f in (lambda y : chr(y), lambda y : chr(y + 32))]
atomic_propositions.extend(['⊤','⊥'])

connectives = ['¬','∧','∨','⇒','⇔']
priority = {'⇔':1,'⇒':2,'∨':3,'∧':3,'¬':4}

digits = ['0','1','2','3','4','5','6','7','8','9']

class Tree:
    def __init__(self,name):
        self.name = name
        self.children = []
        self.parent = 0
        self.ispos = 0
        self.depth = 0

    def append(self,childName):
        Node = Tree(childName)
        Node.parent = self
        Node.depth = self.depth+1
        self.children.append(Node)

    def visualize(self):
        output = "  "*self.depth + self.name + "<--"*self.ispos + '\n'
        for child in self.children:
            output += child.visualize()
        return output

    def polish(self):
        output = self.name
        if self.name in ['∧','∨']:
            output += '('

        for child in self.children:
            output += child.polish()
            
        if self.name in ['∧','∨']:
            output += ')'
        return output

def parsePolish(Node):
    global Pos,Q,i
    Pos.ispos = 0
    Pos = Node
    Pos.ispos = 1
    f.write("Symbol:{}\n".format(Q[i]))
    f.write(T.visualize()+'\n')
    Pos.name = Q[i]
    if Q[i][0] in connectives:
        if Q[i][0] == '¬':
            Pos.append("\"F\"")
            i += 1
            parsePolish(Pos.children[0])

        elif Q[i][0] in ['∧','∨']:
            origin = Q[i][0]
            Pos.append("\"F\"")
            Pos.append("\"F\"")
            openNodes = 2
            while openNodes > 0:
                i += 1
                if Q[i] == origin:
                    f.write("Symbol:{}\n".format(Q[i]))
                    f.write(T.visualize()+'\n')
                    Pos.append("\"F\"")
                    Pos.children.insert(0, Pos.children.pop())
                    openNodes += 1
                else:
                    parsePolish(Pos.children[openNodes - 1])
                    openNodes -= 1
            
        else:
            Pos.append("\"F\"")
            Pos.append("\"F\"")

            i += 1
            parsePolish(Pos.children[1])
            i += 1
            parsePolish(Pos.children[0])
    
    Pos.ispos = 0
    Pos = Node.parent
    if Pos != 0:
        Pos.ispos = 1

with open("parseR_In.txt",'r', encoding="UTF-8") as f:
    exps = f.readlines()

f = open("parseR_Out.txt",'w', encoding="UTF-8")
nrs = [chr(48 + i) for i in range(10)]
for exp in exps:
    state = "Well-formed"
    exp = exp.strip("\n ")
    f.write(exp + "\n\n")
    Q = []
    S = []

    d = [['(','¬',"var"],[')','∧','∨','⇒','⇔']]  
    expect = 0
    f.write("Expect:{}\nQueue:{}\nStack:{}\n\n".format(d[expect],Q,S))

    if exp[-1] != ')' and exp[-1] not in atomic_propositions and exp[-1] not in digits:
        state = "Not well-formed: A well-formed propositional formula in relaxed syntax may only end with a closed paranthesis or a propositional variable."

    l = len(exp)
    i = 0
    while i < l:
        symb = exp[i]
        if state != "Well-formed":
            break

        if symb != ' ':
            f.write("Symbol:'{}'\nExpect:{}\n".format(symb,d[expect]))

            if symb in atomic_propositions:
                i += 1
                while i < l and exp[i] in nrs:
                    symb += exp[i]
                    i += 1
                i -= 1
                if expect == 0:
                    Q.append(symb)
                    expect = 1
                else:
                    state = "Not well-formed: Expected a different symbol here."

            elif symb in connectives:
                if (expect == 1 and symb != '¬') or (expect == 0 and symb == '¬'):
                    if len(S) == 0 or S[-1] == '(':
                        S.append(symb)
                    else:
                        while len(S) != 0 and S[-1] != '(' and priority[symb] < priority[S[-1]]:
                            Q.append(S[-1])
                            S.pop()
                        S.append(symb)
                    expect = 0
                else:
                    state = "Not well-formed: Expected a different symbol here."

            elif symb == '(':
                if expect == 0:
                    S.append(symb)
                else:
                    state = "Not well-formed: Expected a different symbol here."

            elif symb == ')':
                if expect == 1:
                    if len(S) == 0:
                        state = "Not well-formed: Proposition contains an unclosed right parenthesis."
                    elif S[-1] == '(':
                        state = "Not well-formed: Unnecessary parentheses"
                    else:
                        while len(S) != 0 and S[-1] != '(':
                            Q.append(S[-1])
                            S.pop()
                        if len(S) == 0:
                            state = "Not well-formed: Proposition contains an unclosed right parenthesis."
                        else:
                            S.pop()
                else:
                    state = "Not well-formed: Expected a different symbol here."

            else:
                state = "Not well-formed: Proposition contains undefined symbols."

            f.write("Queue:{}\nStack:{}\n\n".format(Q,S))
        i += 1
    if state == "Well-formed":
        while len(S) != 0 and S[-1] != '(':
            Q.append(S[-1])
            S.pop()
        if len(S) != 0:
            f.write("Queue:{}\nStack:{}\n\n".format(Q,S))
            state = "Not well-formed: Proposition contains an unclosed left parenthesis."

    if state == "Well-formed":
        Q.reverse()
        f.write("Queue:{}\nStack:{}\n\n".format(Q,S))

        i = 0
        T = Tree("\"F\"")
        Pos = T
        parsePolish(T)

        f.write(T.visualize()+'\n')
        f.write(T.polish()+"\n\n")
        f.write("Well-formed propositional formula when using relaxed syntax.\n\n")
    else:
        f.write("".join([state,"\n\n"]))

f.close()