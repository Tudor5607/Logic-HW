import copy

atomic_propositions = [f(x) for x in range(65,91) for f in (lambda y : chr(y), lambda y : chr(y + 32))]
atomic_propositions.extend(['⊤','⊥'])

connectives = ['¬','∧','∨','⇒','⇔']
priority = {'⇔':1,'⇒':2,'∨':3,'∧':3,'¬':4}
flip = {'∧':'∨', '∨':'∧'}
teXsymb = {'⊤':r"\top", '⊥':r"\bot", '¬':r"\lnot ", '∧':r"\land", '∨':r"\lor", '⇒':r"\Rightarrow", '⇔':r"\Leftrightarrow", '□':r"\square"}
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

    def append(self,childName):
        Node = Tree(childName)
        Node.parent = self
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
    global p,i
        
    Node.name = p[i]
    if p[i][0] in connectives:
        if p[i][0] == '¬':
            Node.append("\"F\"")
            i += 1
            parsePolish(Node.children[0])

        elif p[i][0] in ['∧','∨']:
            i += 2
            while p[i][0] != ')':
                Node.append("\"F\"")
                parsePolish(Node.children[-1])
                i += 1
            
        else:
            Node.append("\"F\"")
            Node.append("\"F\"")

            i += 1
            parsePolish(Node.children[0])
            i += 1
            parsePolish(Node.children[1])
    else:
        l = len(p)
        i += 1
        while i < l and p[i] in nrs:
            Node.name += p[i]
            i += 1
        i -= 1

def Negate(Node):
    if Node.name in flip:
        Node.name = flip[Node.name]
        for i in range(len(Node.children)):
            Negate(Node.children[i])
    else:
        if Node.name == '¬':
            Node.name = Node.children[0].name
            Node.children = []
        else:
            aux = Tree(Node.name)
            aux.parent = Node
            Node.children = [aux]
            Node.name = '¬'

def combine(Node):
    i = 0
    l = len(Node.children)

    while i < l:
        if Node.name == Node.children[i].name:
            j = i
            for child in Node.children[i].children:
                i += 1
                child.parent = Node
                Node.children.insert(i,child)
            Node.children.pop(j)
            i -= 1
            l = len(Node.children)

        i += 1

def DNF(Node):
    global og
    for child in Node.children:
        DNF(child)

    if Node.name in flip:
        combine(Node)

    if Node.name == '∧':
        for i in range(len(Node.children)):
            if Node.children[i].name == '∨':
                cdeep = copy.deepcopy(Node.children[i].children)
                temp = copy.deepcopy(Node.children)
                Node.name = '∨'
                Node.children = []
                for lit in cdeep:
                    c = copy.deepcopy(temp)
                    c.pop(i)
                    aux = Tree('∧')
                    for cc in c:
                        cc.parent = aux

                    aux.parent = Node
                    lit.parent = aux
                    aux.children = [lit]
                    aux.children.extend(c)
                    Node.children.append(aux)

                f.write(r" \sim " + lateXfy(og.visualize()))
                DNF(Node)
                break


with open("DorCNF_In.txt",'r', encoding="UTF-8") as f:
    Prop = f.readlines()

f = open("DorCNF_Out.txt",'w', encoding="UTF-8")

for p in Prop:
    p = p.strip(" \n")
    T = Tree("")
    i = 0
    changed = 0
    parsePolish(T)
    Q = copy.deepcopy(T)
    orig = lateXfy(Q.visualize())
    f.write(r"DNF:\\" + '\n' + '$')
    f.write(lateXfy(T.visualize()))
    og = T
    DNF(T)
    f.write(r" \sim " + lateXfy(T.visualize()))
    f.write(r"$\\ \\" + "\n\n")

    f.write(r"CNF:\\" + '\n' + '$')

    f.write(r" \lnot(" + lateXfy(Q.visualize()) + ')')
    Negate(Q)
    f.write(r" \sim " + lateXfy(Q.visualize()))
    og = Q
    DNF(Q)
    f.write(r" \sim " + lateXfy(Q.visualize()))
    Negate(Q)
    f.write(r"$\\ So: \\$" + orig + r" \sim " + lateXfy(Q.visualize()))
    f.write(r"$\\" + "\n\n")


f.close()