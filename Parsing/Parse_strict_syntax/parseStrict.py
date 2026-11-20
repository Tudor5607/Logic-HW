atomic_propositions = [f(x) for x in range(65,91) for f in (lambda y : chr(y), lambda y : chr(y + 32))]
atomic_propositions.extend(['⊤','⊥'])

nrs = [chr(48 + i) for i in range(10)]
connectives = ['¬','∧','∨','⇒','⇔']
teXsymb = {'⊤':r" \top ", '⊥':r" \bot ", '¬':r" \lnot ", '∧':r" \land ", '∨':r" \lor ", '⇒':r" \Rightarrow ", '⇔':r" \Leftrightarrow ", '□':r" \square "}

def lateXfy(text):
    l = len(text)
    i = 0
    while i < l:
        if text[i] in atomic_propositions:
            i += 1
            if i < l and text[i] in nrs:
                j = i
                while i < l and text[i] in nrs:
                    i += 1
                text = text[:j] + "_{" + text[j:i] + '}' + text[i:]
                l = len(text)
            i -= 1
        i +=  1

    for s in teXsymb.keys():
        text = text.replace(s,teXsymb[s])

    return text

class Tree:
    def __init__(self,name):
        self.name = name
        self.children = []
        self.parent = 0
        self.ispos = 0

    def append(self,childName):
        Node = Tree(childName)
        Node.parent = self
        self.children.append(Node)

    def visualize(self):
        output = "[$" + self.ispos*r"\textcolor{red}{" + lateXfy(self.name) + self.ispos*'}' + "$"
        for child in self.children:
            output += child.visualize()
        output += ']'
        return output

def movePosUp():
    global Pos
    Pos.ispos = 0
    Pos = Pos.parent
    if Pos != 0:
        Pos.ispos = 1

def movePosDown():
    global Pos,state
    Pos.ispos = 0
    for child in Pos.children:
        if child.name == "\"F\"":
            Pos = child
            Pos.ispos = 1
            break

def step(symbol):
    global Pos,state

    if symbol == '(':
        if Pos.name == "\"F\"":
            Pos.name = "\"□\""
            Pos.append("\"F\"")
            movePosDown()
        else:
            state = "Not well-formed: Didn't expect a '(' here."

    elif symbol[0] in atomic_propositions:
        if Pos.name == "\"F\"":
            Pos.name = symbol
            movePosUp()
        else:
            state = "Not well-formed: Didn't expect an atom here."

    elif symbol in connectives:
        if symbol == '¬' and Pos.parent  != 0:
            if Pos.name == "\"F\"" and Pos.parent.name == "\"□\"":
                Pos.parent.name = '¬'
            else:
                state = "Not well-formed: Didn't expect a negation here."
        elif symbol == '¬':
            state = "Not well-formed: Didn't expect a negation here."

        else:
            if (symbol in ['∧','∨'] and Pos.name == symbol) or Pos.name == "\"□\"":
                Pos.name = symbol
                Pos.append("\"F\"")
                movePosDown()
            else:
                state = "Not well-formed: Didn't expect binary connective here."

    elif symbol == ')':
        if Pos.name in connectives:
            movePosUp()
        else:
            state = "Not well-formed: Didn't expect a ')' here."

    else:
        state = "Not well-formed: The string contains symbols that cannot appear in a propositional formula. ({})".format(symbol)

with open("parseS_In.txt",'r', encoding="UTF-8") as f:
    inpt = f.readlines()

f = open("parseS_Out.txt",'w', encoding="UTF-8")

f.write(r"\documentclass{article}" + '\n')
f.write(r"\usepackage[margin=2cm]{geometry}" + '\n')
f.write(r"\usepackage{forest}" + '\n')
f.write(r"\usepackage{amssymb}" + "\n\n")
f.write(r"\begin{document}" + '\n')
	

for exp in inpt:
    state = "Well-formed"
    exp = exp.strip("\n ")
    f.write(r"\noindent" + '\n')
    f.write('$' + lateXfy(exp) + '$' + "\\\\ \\\\" + '\n')

    prop = Tree("\"F\"")
    Pos = prop
    Pos.ispos = 1
    stp = 0

    i = 0
    l = len(exp)
    while i < l:
        symbol = exp[i]
        if symbol in atomic_propositions:
            i += 1
            while i < l and exp[i] in nrs:
                symbol += exp[i]
                i += 1
            i -= 1

        if symbol != ' ' and Pos != 0:
            f.write("Step {}, Symbol '${}$':\\\\ \n".format(stp,lateXfy(symbol)))

            step(symbol)
                
            f.write(r"\begin{forest}" + prop.visualize() + r"\end{forest}" + "\\\\ \n")

            if state != "Well-formed":
                break
            
            stp += 1
        elif Pos == 0:
            state = "Not well-formed: We exited the tree too early."
            break
        i += 1

    if state == "Well-formed" and Pos != 0:
        state = "Not well-formed: We haven't exited the tree."

    f.write(r"\noindent" + '\n')
    f.write(state + "\\\\ \\\\" + "\n\n\n")

f.write(r"\end{document}" + '\n')

f.close()