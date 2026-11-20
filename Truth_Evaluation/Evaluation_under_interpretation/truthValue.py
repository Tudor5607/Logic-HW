atomic_propositions = [f(x) for x in range(65,91) for f in (lambda y : chr(y), lambda y : chr(y + 32))]
atomic_propositions.extend(['⊤','⊥'])

connectives = ['¬','∧','∨','⇒','⇔']
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

    def delete_descendents(self):
        self.children = []

def evaluate(Node,endLevel,v):
    if Node.depth == endLevel:
        if isAtomic(Node.name):
            Node.name = str(v[Node.name])

        elif Node.name == '¬':
            Node.name = str(not str_to_bool(Node.children[0].name))
            Node.delete_descendents()

        elif Node.name == '∧':
            Node.name = str(str_to_bool(Node.children[0].name) and str_to_bool(Node.children[1].name))
            Node.delete_descendents()

        elif Node.name == '∨':
            Node.name = str(str_to_bool(Node.children[0].name) or str_to_bool(Node.children[1].name))
            Node.delete_descendents()

        elif Node.name == '⇒':
            Node.name = str((not str_to_bool(Node.children[0].name)) or str_to_bool(Node.children[1].name))
            Node.delete_descendents()

        elif Node.name == '⇔':
            op1 = (not str_to_bool(Node.children[0].name)) or str_to_bool(Node.children[1].name)
            op2 = (not str_to_bool(Node.children[1].name)) or str_to_bool(Node.children[0].name)
            Node.name = str(op1 and op2)
            Node.delete_descendents()

    else:
        for child in Node.children:
            evaluate(child,endLevel,v)


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

for p in Prop:
    T = Tree("\"F\"")
    i = 0
    depth = 0
    parsePolish(T)
    print(T.visualize())
    #for i in range(depth,-1,-1):
    #    evaluate(T,i,d)
    #    f.write(T.visualize() + '\n')
        
f.close()