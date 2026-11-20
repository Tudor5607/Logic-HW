import copy

#\documentclass[12pt]{article}
#\usepackage[top=0.5cm, left=1cm, right=1cm]{geometry}
#\usepackage{amsmath}
#\usepackage{amssymb}
#\usepackage{amsthm}
#\usepackage{mathrsfs}
#\usepackage{xcolor}
#\usepackage{extarrows}
#\usepackage{graphicx}

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

def NNF1(Pos):
    global changed
    if Pos.children != []:
        if Pos.name == '⇔':
            Pos.name = '∧'

            paux0 = Tree('⇒')
            paux0.parent = Pos
            Pos.children[0].parent = paux0
            Pos.children[1].parent = paux0
            paux0.children = [Pos.children[0],Pos.children[1]]

            aux0 = copy.deepcopy(Pos.children[0])
            aux1 = copy.deepcopy(Pos.children[1])
            paux1 = Tree('⇒')
            paux1.parent = Pos
            aux0.parent = paux1
            aux1.parent = paux1
            paux1.children = [aux1,aux0]
            
            Pos.children = [paux0,paux1]
            changed = 1

        for child in Pos.children:
            NNF1(child)

def NNF2(Pos):
    global changed

    if Pos.children != []:
        if Pos.name == '⇒':
            Pos.name = '∨'
            aux0 = Tree('¬')
            aux0.parent = Pos
            aux0.children = [Pos.children[0]]
            Pos.children[0].parent = aux0
            Pos.children = [aux0,Pos.children[1]]
            changed = 1

        for child in Pos.children:
            NNF2(child)

def NNF3(Pos):
    global changed

    if Pos.name == '¬':
        child = Pos.children[0]

        if child.name == '¬':
            inner = child.children[0]
            Pos.name = inner.name
            Pos.children = inner.children
            for c in Pos.children:
                c.parent = Pos
            NNF3(Pos)
            changed = 1
            return

        elif child.name in flip:
            Pos.name = flip[child.name]
            aux = []
            for c in child.children:
                aux0 = Tree('¬')
                aux0.parent = Pos
                aux0.children = [c]
                c.parent = aux0
                aux.append(aux0)
            Pos.children = aux
            changed = 1

    for child in Pos.children:
        NNF3(child)

def NNF4(node):
    for c in node.children:
        NNF4(c)
    if node.name in ['∧', '∨']:
        new = []
        for c in node.children:
            if c.name == node.name:
                for g in c.children:
                    g.parent = node
                new.extend(c.children)
            else:
                new.append(c)
        node.children = new

with open("NNF_In.txt",'r', encoding="UTF-8") as f:
    Prop = f.readlines()

f = open("NNF_Out.txt",'w', encoding="UTF-8")

for p in Prop:
    p = p.strip(" \n")
    T = Tree("")
    i = 0
    changed = 0
    parsePolish(T)
    f.write(r"NNF:\\" + '\n' + '$')
    f.write(lateXfy(T.visualize()))

    changed = 0
    NNF1(T)
    if changed == 1:
        f.write(r" \sim " + lateXfy(T.visualize()))

    changed = 0
    NNF2(T)
    if changed == 1:
        f.write(r" \sim " + lateXfy(T.visualize()))
    

    changed = 0
    NNF3(T)
    if changed == 1:
        f.write(r" \sim " + lateXfy(T.visualize()))

    changed = 0
    NNF4(T)
    if changed == 1:
        f.write(r" \sim " + lateXfy(T.visualize()))
    

    f.write(r"$\\ \\" + "\n\n")


f.close()