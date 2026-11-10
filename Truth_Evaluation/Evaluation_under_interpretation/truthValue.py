#Will be used to construct a tree object.
class Tree:
    #Constructor.
    def __init__(self,name):
        self.name = name
        self.children = []
        self.parent = 0
        self.ispos = 0
        self.depth = 0

    #Append a new subtree.
    def append(self,childName):
        Node = Tree(childName)
        Node.parent = self
        Node.depth = self.depth+1
        self.children.append(Node)

    #Returns a string that is a visualization of the tree, along with our position in the tree (if it exists).
    def visualize(self):
        output = "  "*self.depth + self.name + "<--"*self.ispos + '\n'
        for child in self.children:
            output += child.visualize()
        return output

    #Removes all descendents of this node
    def delete_descendents(self):
        self.children = []

#Generates all possible interpretations for the list of variables "vars" by using the method of binary counting.
def generateInterpretations(vars):
    I = {}
    for var in vars:
        I[var] = "False"
    yield I
    for i in range(2**len(vars)-1):
        for var in vars:
            if I[var] == "False":
                I[var] = "True"
                yield I
                break
            else:
                I[var] = "False"

#Checks if the symbol is an atomic proposition.
def isAtomic(symbol):
    if ('a' <= symbol <= 'z') or ('A' <= symbol <= 'Z'):
        return True
    return False

#Checks if the symbol is a logical connective.
def isConnective(symbol):
    if symbol == '¬' or symbol == '∧' or symbol == '∨' or symbol == '⇒' or symbol == '⇔':
        return True
    return False

#Converts a string representing a truth value to that truth value
def str_to_bool(value):
    if value == "True":
        return True
    return False

#Used to evaluate a proposition based on its abstract syntax. The evaluation is done only on level "endLevel". (v is our chosen interpretation)
#Note that this function assumes that the tree already has a particular form.
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

#Converts from polish notation (input) to a tree. Also helps us determine the maximum depth
def fill(Node,Q):
    global Pos,T,i,depth
    if Node.depth > depth:
        depth = Node.depth
    Pos.ispos = 0
    Pos = Node
    Pos.ispos = 1
    if isConnective(Q[i]):
        if Q[i] == '¬':
            Pos.name = '¬'
            Pos.append("\"F\"")

            i += 1
            fill(Pos.children[0],Q)
        else:
            Pos.name = Q[i]
            Pos.append("\"F\"")
            Pos.append("\"F\"")

            i += 1
            fill(Pos.children[0],Q)
            i +=1
            fill(Pos.children[1],Q)
    else:
        Node.name = Q[i]
    
    Pos.ispos = 0
    Pos = Node.parent
    if Pos != 0:
        Pos.ispos = 1

with open("truthValue_In.txt",'r', encoding="UTF-8") as f:
    Prop = f.readlines()

I = Prop[-1].split()
Prop = Prop[:-1]
Prop = [w.strip("\n ") for w in Prop]
f = open("truthValue_Out.txt",'w', encoding="UTF-8")
d = {}
for pair in I:
    if pair[2] == 'T':
        d[pair[0]] = "True"
    else:
        d[pair[0]] = "False"
for p  in Prop:
    T = Tree("\"F\"")
    Pos = T
    i = 0
    depth = 0
    fill(T,p)
    f.write(T.visualize() + '\n')
    for i in range(depth,-1,-1):
        evaluate(T,i,d)
        f.write(T.visualize() + '\n')
        
f.close()