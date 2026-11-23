atomic_propositions = [f(x) for x in range(65,91) for f in (lambda y : chr(y), lambda y : chr(y + 32))]
atomic_propositions.extend(['⊤','⊥'])

connectives = ['¬','∧','∨','⇒','⇔']
priority = {'⇔':1,'⇒':2,'∨':3,'∧':3,'¬':4}
teXsymb = {'⊤':r"\top", '⊥':r"\bot", '¬':r"\lnot ", '∧':r"\land", '∨':r"\lor", '⇒':r"\Rightarrow", '⇔':r"\Leftrightarrow", '∼':r"\sim", '⊨':r"\vDash", '⊤':r"\top", '⊥':r"\bot"}
nrs = [chr(48 + i) for i in range(10)]

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
        self.depth = 0

    def append(self,childName):
        Node = Tree(childName)
        Node.parent = self
        Node.depth = self.depth + 1
        self.children.append(Node)

    def visualize(self):
        output = ''
        par = self.parent
        needs_paren = (
            self.name in connectives and self.name != '¬' and par != 0 and (
                priority[par.name] > priority[self.name]
                or (priority[par.name] == priority[self.name]
                    and self is not par.children[-1])
                or (self.name in ['∧', '∨'] and par.name in ['∧', '∨']
                    and self.name != par.name)
            )
        )
        if needs_paren:
            output += '(' + (' ' + self.name + ' ').join([child.visualize() for child in self.children]) + ')'
        elif self.name in connectives and self.name != '¬':
            output += (' ' + self.name + ' ').join([child.visualize() for child in self.children])
        elif self.name == '¬':
            output += '¬' + self.children[0].visualize()
        else:
            output += self.name
        return output


def parsePolish(Node):
    global Q,i,depth

    if Node.depth > depth:
        depth = Node.depth

    Node.name = Q[i]
    if Q[i][0] in connectives:
        if Q[i][0] == '¬':
            Node.append("\"F\"")
            i += 1
            parsePolish(Node.children[0])

        elif Q[i][0] in ['∧','∨']:
            origin = Q[i][0]
            Node.append("\"F\"")
            Node.append("\"F\"")
            openNodes = 2
            while openNodes > 0:
                i += 1
                if Q[i] == origin:
                    Node.append("\"F\"")
                    Node.children.insert(0, Node.children.pop())
                    openNodes += 1
                else:
                    parsePolish(Node.children[openNodes - 1])
                    openNodes -= 1
            
        else:
            Node.append("\"F\"")
            Node.append("\"F\"")

            i += 1
            parsePolish(Node.children[1])
            i += 1
            parsePolish(Node.children[0])

def generateInterpretations(vars):
    I = {}
    for var in vars:
            I[var] = False
    yield I
    for i in range(2**len(vars)-1):
        for var in vars:
            if I[var] == False:
                I[var] = True
                yield I
                break
            else:
                I[var] = False


#Creates a table of all interpretations of this proposition under all interpretations. Warning it does change the current tree it is applied on.
def table_first_row(depth):
        global d,Pos,tab
        t = tab[0]

        if Pos.depth == depth:
            aux = Pos.visualize()
            if aux not in t:
                t.append(aux)
                d[aux] = [t.index(child.visualize()) for child in Pos.children]
                d[aux].append(Pos.name)

        else:
            for child in Pos.children:
                Pos = child
                table_first_row(depth)

with open("table_In.txt",'r', encoding="UTF-8") as f:
    exps = f.readlines()

f = open("table_Out.txt",'w', encoding="UTF-8")
#Don't mind this
#f.write(r"\documentclass{article}" + '\n')
#f.write(r"\usepackage{amssymb}   % \mathbb, \vDash" + '\n')
#f.write(r"\usepackage{xcolor}    % \textcolor{red}" + '\n')
#f.write(r"\begin{document}" + "\n\n")

for exp in exps:

    exp = exp.strip(" \n")
    Q = []
    S = []
    d = {}
    sav = exp
    #Cases for logical equivalence and consequence
    if '∼' in exp:
        j = exp.index('∼')
        exp = '(' + exp[0:j-1] + ') ⇔ (' + exp[j+2:] + ')'

    if '⊨' in exp:
        exp = exp.replace(",",") ∧ (")
        j = exp.index('⊨')
        exp = '(' + exp[0:j-1] + ') ⇒ (' + exp[j+2:] + ')'

    Leaves = []

    for i in range(len(exp)):
        symb = exp[i]

        if symb != ' ':

            if symb in atomic_propositions:
                i += 1
                while i < len(exp) and exp[i] in nrs :
                    symb += exp[i]
                    i += 1
                if symb not in Leaves:
                    Leaves.append(symb)
                Q.append(symb)

            elif symb in connectives:
                if len(S) == 0 or S[-1] == '(':
                    S.append(symb)
                else:
                    while len(S) != 0 and S[-1] != '(' and priority[symb] < priority[S[-1]]:
                        Q.append(S[-1])
                        S.pop()
                    S.append(symb)

            elif symb == '(':
                S.append(symb)

            elif symb == ')':
                while len(S) != 0 and S[-1] != '(':
                    Q.append(S[-1])
                    S.pop()
                S.pop()

    while len(S) != 0 and S[-1] != '(':
        Q.append(S[-1])
        S.pop()
    Q.reverse()

    i = 0
    depth = 0
    T = Tree("\"F\"")
    parsePolish(T)

    tab = [[]]
    tab[0].extend(Leaves)
    for i in range(depth,-1,-1):
        Pos = T
        table_first_row(i)

    excluded = []
    if '⊤' in Leaves:
        Leaves.pop(Leaves.index('⊤'))
        excluded.append('⊤')

    if '⊥' in Leaves:
        Leaves.pop(Leaves.index('⊥'))
        excluded.append('⊥')

    g = generateInterpretations(Leaves)
    for i in range(1,2**(len(Leaves))+1):
        tab.append([])
        I = next(g)
        I['⊤'] = True
        I['⊥'] = False

        for j in range(len(Leaves) + len(excluded)):
            tab[i].append(I[tab[0][j]])

        for j in range(len(Leaves) + len(excluded),len(tab[0])):

            if d[tab[0][j]][-1] == '¬':
                ind = d[tab[0][j]][0]
                tab[i].append(not tab[i][ind])

            elif d[tab[0][j]][-1] == '∧':
                aux = True
                for ind in d[tab[0][j]][:-1]:
                    if tab[i][ind] == False:
                        aux = False
                        break
                tab[i].append(aux)

            elif d[tab[0][j]][-1] == '∨':
                aux = False
                for ind in d[tab[0][j]][:-1]:
                    if tab[i][ind] == True:
                        aux = True
                        break
                tab[i].append(aux)

            elif d[tab[0][j]][-1] == '⇒':
                ind = d[tab[0][j]][0]
                jnd = d[tab[0][j]][1]
                if tab[i][ind] == True and tab[i][jnd] == False:
                    tab[i].append(False)
                else:
                    tab[i].append(True)

            elif d[tab[0][j]][-1] == '⇔':
                ind = d[tab[0][j]][0]
                jnd = d[tab[0][j]][1]
                if tab[i][ind] ==  tab[i][jnd]:
                    tab[i].append(True)
                else:
                    tab[i].append(False)

    #Changing into latex comptatible syntax
    exp = lateXfy(sav)

    f.write(r"\noindent" + '\n')
    f.write('$' + exp + '$' + r" \\" + '\n')

    #Optional in case tables get too big.
    #f.write(r"\normalsize" + '\n')
    f.write(r"\noindent" + '\n')
    f.write(r"\begin{tabular}{ " + r"|c"*len(tab[0]) + r"| } " + '\n')

    for i in range(len(tab[0])):
        tab[0][i] = tab[0][i].replace('⊤', r"\top")
        tab[0][i] = tab[0][i].replace('⊥', r"\bot")

    for i in range(len(tab)):
        l = len(tab[i]) - 1
        for j in range(len(tab[i])):

            if tab[i][j] == True:
                if j == l:
                    tab[i][j] = r"$\textcolor{red}{\mathbb{T}}$"
                else:
                    tab[i][j] = r"$\mathbb{T}$"
            elif tab[i][j] == False:
                if j == l:
                    tab[i][j] = r"$\textcolor{red}{\mathbb{F}}$"
                else:
                    tab[i][j] = r"$\mathbb{F}$"
            else:
                tab[i][j] = tab[i][j].replace('¬',r"\lnot ")
                tab[i][j] = tab[i][j].replace('∧',r"\land")
                tab[i][j] = tab[i][j].replace('∨',r"\lor")
                tab[i][j] = tab[i][j].replace('⇒',r"\Rightarrow")
                tab[i][j] = '$' + tab[i][j].replace('⇔',r"\Leftrightarrow") + '$'
        f.write(r"\hline" + '\n')
        f.write(" & ".join([lateXfy(a) for a in tab[i]]) + r" \\" +'\n')

    f.write(r"\hline")
    f.write(r"\end{tabular}\\ \\" + "\n\n")
    #f.write(r"\large" + '\n')


#f.write("\n\n" + r"\end{document}")


f.close()