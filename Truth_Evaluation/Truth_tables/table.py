#Generates all possible interpretations for the list of variables "vars" by using the method of binary counting.
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

#Will be used to construct a tree object.
class Tree:
    #Constructor.
    def __init__(self,name):
        self.name = name
        self.children = []
        self.parent = 0
        self.depth = 0
        self.dom = 0
        self.table_nr = 1.1

    #Append a new subtree.
    def append(self,childName):
        Node = Tree(childName)
        Node.parent = self
        Node.depth = self.depth+1
        self.children.append(Node)

    #Returns a string that is a visualization of the tree in polish notation. (recommended only for complete trees)
    def polish(self):
        output = self.name
        for child in self.children:
            output += child.polish()
        return output

    #Returns a string that is a visualization of the tree, along with our position in the tree (if it exists).
    def visualize(self):
        output = "  "*self.depth + self.name + '\n'
        for child in self.children:
            output += child.visualize()
        return output

    #Returns a list containiing the leaves of the tree that had this node as root, from left to right, also sets up positions for the table.
    def getLeaves(self):
        global Leaves
        if self.children == []:
            if self.name not in Leaves:
                self.table_nr = len(Leaves)
                Leaves.append(self.name)
        else:
            for child in self.children:
                child.getLeaves()
        return Leaves

    #Creates a table of all interpretations of this proposition under all interpretations. Warning it does change the current tree it is applied on.
    def table(self,tab,depth):
        global d

        if self.depth == depth:
            if self.name == '¬':

                if isAtomic(self.children[0].name):
                    self.name = '¬' + self.children[0].name
                else:
                    self.name = '¬' + '(' + self.children[0].name + ')'
                if self.name not in tab:
                    tab.append(self.name)
                    d[self.name] = (tab.index(self.children[0].name),self.dom)


            elif self.children != []:

                left = 0
                right = 0
                #if the dominant operation of subproposition does not take priority over the current operation, we make sure it takes priority by putting a parenthesis around it.
                if self.children[0].dom <= self.dom:
                    left = 1
                if self.children[1].dom <= self.dom:
                    right = 1
                self.name = '('*left + self.children[0].name + ')'*left + ' ' + self.name + ' ' + '('*right + self.children[1].name + ')'*right
                if self.name not in tab:
                    tab.append(self.name)
                    d[self.name] = (tab.index(self.children[0].name),tab.index(self.children[1].name),self.dom)

        else:
            for child in self.children:
                child.table(tab,depth)

#Class used solely to define an order on symbols.
class Symbol:

    priority = {'⇔':1,'⇒':2,'∨':3,'∧':3,'¬':4,' ':5}

    def __init__(self,name):
        self.name = name
    
    def __lt__(self,other):
        return self.priority[self.name] < self.priority[other.name]

    def __le__(self,other):
        return self.priority[self.name] <= self.priority[other.name]

    def __repr__(self):
        return "".join(["'",self.name,"'"])

#Checks if the symbol is an atomic proposition.
def isAtomic(symbol):
    if (('a' <= symbol <= 'z') or ('A' <= symbol <= 'Z') or symbol == '⊤' or symbol == '⊥') and len(symbol) == 1:
        return True
    return False

#Checks if the symbol is a logical connective.
def isConnective(symbol):
    if symbol == '¬' or symbol == '∧' or symbol == '∨' or symbol == '⇒' or symbol == '⇔':
        return True
    return False

#Will be used to attempt to create the abstract syntax after the shunting yard algorithm finishes.
def fill(Node):
    global Q,i,depth

    if Node.depth > depth:
        depth = Node.depth
    
    if isConnective(Q[i]):
        if Q[i] == '¬':
            Node.name = '¬'
            Node.dom = Symbol('¬')
            Node.append("\"F\"")
            
            i += 1
            fill(Node.children[0])
        else:
            Node.name = Q[i]
            Node.dom = Symbol(Q[i])
            Node.append("\"F\"")
            Node.append("\"F\"")

            i += 1
            fill(Node.children[1])
            i += 1
            fill(Node.children[0])
    else:
        Node.name = Q[i]
        Node.dom = Symbol(' ')
    

with open("table_In.txt",'r') as f:
    exps = f.readlines()

f = open("table_Out.txt",'w')
#Don't mind this
#f.write(r"\documentclass{article}" + '\n')
#f.write(r"\usepackage{amssymb}   % \mathbb, \vDash" + '\n')
#f.write(r"\usepackage{xcolor}    % \textcolor{red}" + '\n')
#f.write(r"\begin{document}" + "\n\n")

for exp in exps:

    exp = exp[:-1]
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

    for symb in exp:

        #Spaces are not relevant.
        if symb != ' ':

            #If the symbol is a propositional variable it gets added to the queue.
            if isAtomic(symb) == True:
                Q.append(symb)

            #For logical connectives we may need to check precedence first.  
            elif isConnective(symb):
                A = Symbol(symb)
                if len(S) == 0 or S[-1] == '(':
                    S.append(A)
                else:
                    while len(S) != 0 and S[-1] != '(' and A < S[-1]:
                        Q.append(S[-1].name)
                        S.pop()
                    S.append(A)

            #An open paranthesis doesn't do anything on its own.
            elif symb == '(':
                S.append(symb)

            #A closed paranthesis must have an accompanying open paranthesis to determine the priority of connectives.
            elif symb == ')':
                while len(S) != 0 and S[-1] != '(':
                    Q.append(S[-1].name)
                    S.pop()
                S.pop()

    #We clean the stack after all symbols have ran out.
    while len(S) != 0 and S[-1] != '(':
        Q.append(S[-1].name)
        S.pop()

    Q.reverse()
    i = 0
    depth = 0
    T = Tree("\"F\"")
    fill(T)

    tab = [[]]
    Leaves = []
    T.getLeaves()
    tab[0].extend(Leaves)
    for i in range(depth,-1,-1):
        T.table(tab[0],i)

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

            if d[tab[0][j]][-1].name == '¬':
                ind = d[tab[0][j]][0]
                tab[i].append(not tab[i][ind])

            elif d[tab[0][j]][-1].name == '∧':
                ind = d[tab[0][j]][0]
                jnd = d[tab[0][j]][1]
                tab[i].append(tab[i][ind] and tab[i][jnd])

            elif d[tab[0][j]][-1].name == '∨':
                ind = d[tab[0][j]][0]
                jnd = d[tab[0][j]][1]
                tab[i].append(tab[i][ind] or tab[i][jnd])

            elif d[tab[0][j]][-1].name == '⇒':
                ind = d[tab[0][j]][0]
                jnd = d[tab[0][j]][1]
                tab[i].append((not tab[i][ind]) or tab[i][jnd])

            elif d[tab[0][j]][-1].name == '⇔':
                ind = d[tab[0][j]][0]
                jnd = d[tab[0][j]][1]
                tab[i].append( ( (not tab[i][ind]) or tab[i][jnd] ) and ( (not tab[i][jnd]) or tab[i][ind] ))

    #Changing into latex comptatible syntax
    exp = sav
    exp = exp.replace('¬',r"\lnot ")
    exp = exp.replace('∧',r"\land")
    exp = exp.replace('∨',r"\lor")
    exp = exp.replace('⇒',r"\Rightarrow")
    exp = exp.replace('⇔',r"\Leftrightarrow")
    exp = exp.replace('∼',r"\sim")
    exp = exp.replace('⊨',r"\vDash")
    exp = exp.replace('⊤', r"\top")
    exp = exp.replace('⊥', r"\bot")

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
        f.write(" & ".join(tab[i]) + r" \\" +'\n')

    f.write(r"\hline")
    f.write(r"\end{tabular}\\ \\" + "\n\n")
    #f.write(r"\large" + '\n')


#f.write("\n\n" + r"\end{document}")


f.close()