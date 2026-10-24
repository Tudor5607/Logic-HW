#The tree class that will store our propositions
class Tree:
    #Constructor.
    def __init__(self,name):
        self.name = name
        self.children = []
        self.parent = 0
        self.ispos = 0

    #Append a new subtree.
    def append(self,childName):
        Node = Tree(childName)
        Node.parent = self
        self.children.append(Node)

    #Returns a string that is a visualization of the tree.
    def visualize(self,level):
        output = "  "*level + self.name + '\n'
        for child in self.children:
            output += child.visualize(level + 1)
        return output

    #Used to evaluate the proposition under the interpretations for the propositional variables given by the dictionary v.
    def evaluate(self,v):
        if self.name == '¬':
            return not self.children[0].evaluate(v)
        elif self.name == '∧':
            return self.children[0].evaluate(v) and self.children[1].evaluate(v)
        elif self.name == '∨':
            return self.children[0].evaluate(v) or self.children[1].evaluate(v)
        elif self.name == '⇒':
            return (not self.children[0].evaluate(v)) or self.children[1].evaluate(v)
        elif self.name == '⇔':
            p = self.children[0].evaluate(v)
            q = self.children[1].evaluate(v)
            return (p and q) or ((not p) and (not q))
        else:
            return v[self.name]


#Some auxiliary functions

#Checks if the symbol is an atomic proposition.
def isAtomic(symbol):
    if ('a' <= symbol and symbol <= 'z') or ('A' <= symbol and symbol <= 'Z'):
        return True
    return False

#Checks if the symbol is a logical connective.
def isConnective(symbol):
    if symbol == '¬' or symbol == '∧' or symbol == '∨' or symbol == '⇒' or symbol == '⇔':
        return True
    return False

#Performs one of the steps described in the parsing algorithm depending on the symbol we input.
#We also have to return the variable Pos just in case we switch positions, as anything done to the internal structure of it (and by extention of the original tree) will be changed, but if we change what Pos is "pointing" towards, the function will not do that, and we need to do a reassignment outside the function.
#The step for '(' gets handled separately as we need to know what the symbol after it is in order to perform it correctly.
def step(Pos,symbol):
        
    #If the symbol rerpresents an atomic proposition we write it and move up to the parent node.
    if isAtomic(symbol) == True:
        Pos.name = symbol
        Pos = Pos.parent

    #Logical connectives get written and move down to the first available child of the node.
    elif isConnective(symbol) == True:
        Pos.name = symbol
        for child in Pos.children:
            if child.name == '□':
                Pos = child
                break

    #Closed paranthesis moves us to the parent of the current node.
    elif symbol == ')':
        Pos = Pos.parent
    
    return Pos

#I feel like the name is self explanatory for this one.
def createAbstractSyntax(Trees):
    Trees.append(Tree("□"))
    Pos = Trees[i//2]

    for j in range(len(Prop[i])):
        symbol = Prop[i][j]

        #Separate step for '(' as we need to know if the next symbol is '¬' or another logical connective.
        if symbol == '(':

            #Create a child node but don't switch to it as the next step will write '¬' in the current node.
            if Prop[i][j+1] == '¬':
                Pos.append('□')

            #Create two child nodes for the two propositions the connective connects and switch to the first one.
            else:
                Pos.append('□')
                Pos.append('□')
                for child in Pos.children:
                    if child.name == '□':
                        Pos = child
                        break

        #If we don't have an open paranthesis we can move on to the other cases.
        else:
            Pos = step(Pos,symbol)


#Algorithm that builds the abstract syntax and then evaluates the value of the proposition.
Trees = []
Pos = 0
with open("Interpretation_Input_test.txt",'r') as f:
    Prop = f.readlines()


f = open("Interpretation_Output_test.txt",'w')
i = 0
l = len(Prop)
while i < l:
    v = {}
    
    #Prints the letter denoting our current exercise.
    f.write("".join([Prop[i][0],Prop[i][1],Prop[i][2]," "]))

    #Removes unnecasary characters.
    Prop[i] = Prop[i][4:]

    #Create the dictionary for the interpretations of the propositional variables.
    Prop[i+1] = Prop[i+1].split()
    for pair in Prop[i+1]:
        pair.strip(',.')
        if pair[2] == 'T':
            v[pair[0]] = True
        else:
            v[pair[0]] = False

    createAbstractSyntax(Trees)

    f.write(str(Trees[i//2].evaluate(v)) + "\n")
    i += 2

f.close()