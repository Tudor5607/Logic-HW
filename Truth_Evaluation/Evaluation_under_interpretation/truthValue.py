atomic_propositions = [f(x) for x in range(65,91) for f in (lambda y : chr(y), lambda y : chr(y + 32))]
atomic_propositions.extend(['⊤','⊥'])

connectives = ['¬','∧','∨','⇒','⇔']
priority = {'⇔':1,'⇒':2,'∨':3,'∧':3,'¬':4}
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
    global p,i,depth

    if Node.depth > depth:
        depth = Node.depth
        
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

def evaluate(Node,endLevel,v):
    if Node.depth == endLevel:
        if Node.name in v:
            Node.name = v[Node.name]

        elif Node.name == '¬':
            if Node.children[0].name == True:
                Node.name = False
            else:
                Node.name = True

        elif Node.name == '∧':
            Node.name = True
            for child in Node.children:
                if child.name == False:
                    Node.name = False

        elif Node.name == '∨':
            Node.name = False
            for child in Node.children:
                if child.name == True:
                    Node.name = True
            
        elif Node.name == '⇒':
            if Node.children[0].name == True and Node.children[1].name == False:
                Node.name = False
            else:
                Node.name = True

        elif Node.name == '⇔':
            if Node.children[0].name == Node.children[1].name:
                Node.name = True
            else:
                Node.name = False

        Node.children = []

        if Node.name == True:
            return r"\mathbb{T}"
        else:
            return r"\mathbb{F}"
    else:
        if Node.name in connectives:
            output = r"\mathcal{B}" + "_{}(".format(teXsymb[Node.name])
            output += ','.join(evaluate(c,endLevel,v) for c in Node.children) + ')'
            return output
        else:
            output = r"v_{\mathcal{I}}(" + lateXfy(Node.name) + ')'
            return output
    

with open("truthValue_In.txt",'r', encoding="UTF-8") as f:
    Prop = f.readlines()

I = Prop[-1].split()
I = I[1:]
Prop = Prop[:-1]
Prop = [w.strip("\n ") for w in Prop]
f = open("truthValue_Out.txt",'w', encoding="UTF-8")
d = {}
for pair in I:
    pair = pair.split(':')
    if pair[1][0] == 'T':
        d[pair[0]] = True
    else:
        d[pair[0]] = False
d['⊤'] = True 
d['⊥'] = False

for p in Prop:
    T = Tree("\"F\"")
    i = 0
    depth = 0
    parsePolish(T)
    f.write(r"v_{\mathcal{I}}(" + lateXfy(T.visualize()) + r")=\\")
    for i in range(depth + 1,-1,-1):
        f.write(evaluate(T,i,d) + r'=\\')
    f.seek(f.tell() - 3)
    f.write(r"\\ \\" + '\n')
        
f.close()