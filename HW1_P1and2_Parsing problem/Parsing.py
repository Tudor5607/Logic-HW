#The tree class that will be used in the algorithm for determinig whether a string of symbols from the vocabulary of propositional logic is a proposition.
class Tree:
    #Constructor.
    def __init__(self,name):
        self.name = name
        self.children = []
        self.parent = 0
        self.ispos = 0

    #Append a new node.
    def append(self,childName):
        Node = Tree(childName)
        Node.parent = self
        self.children.append(Node)

    #Returns a string that is a visualization of tree, along with our current position inside it.
    def visualize(self,level):
        output = "    "*level + self.name + self.ispos*"<- Current position" + '\n'
        for child in self.children:
            output += child.visualize(level + 1)
        return output

    #Renames the current node if it is "empty", if it fails (the node isn't empty) the algorithm we will change the state (here named "output") of the tree to invalid.
    def rename(self,newName):
        output = "Valid"
        if self.name == '□':
            self.name = newName
        else:
            output = "Invalid"
        return output

    #To be used after we exit the tree succesfully in order to determine if any nodes are "empty".
    def validate(self):
        if self.name == '□':
            return False
        for child in self.children:
            if child.validate() == False:
                return False
        return True


#Some functions used in order to manipulate the trees in the algorithm

#Checks if the symbol is a letter, which means we have reached an atomic propositon.
def isAtomic(symbol):
    if ('a' <= symbol and symbol <= 'z') or ('A' <= symbol and symbol <= 'Z'):
        return True
    return False

#Checks if the symbol is a logical connective.
def isConnective(symbol):
    if symbol == '¬' or symbol == '∧' or symbol == '∨' or symbol == '⇒' or symbol == '⇔':
        return True
    return False

#Performs one of the steps described in the parsing algorithm depending on the symbol we input, it may change the state of the tree to "Ivalid" if any of the steps cannot be performed properly.
#We also have to return the variable Pos just in case we switch positions, as anything done to the internal structure of it (and by extention of the original tree) will be changed, but if we change what Pos is "pointing" towards, the function will not do that, and we need to do a reassignment outside the function.
#The step for '(' gets handled separately as we need to know what the symbol after it is in order to perform it correctly.
def step(Pos,symbol):
    output = "Valid"

    #Blank space does nothing.
    if symbol == ' ':
        pass
        
    #If the symbol rerpresents an atomic proposition we write it and move up to the parent node.
    elif isAtomic(symbol) == True:
        output = Pos.rename(symbol)
        Pos.ispos = 0
        Pos = Pos.parent
        if Pos != 0:
            Pos.ispos = 1

    #Logical connectives get written and move down to the first available child of the node.
    elif isConnective(symbol) == True:
        output = Pos.rename(symbol)
        ok = 0
        for child in Pos.children:
            if child.name == '□':
                ok = 1
                Pos.ispos = 0
                Pos = child
                Pos.ispos = 1
                break
        if ok == 0 and output == "Valid":
            output = "Invalid"

    #Closed paranthesis moves us to the parent of the current node.
    elif symbol == ')':
        Pos.ispos = 0
        Pos = Pos.parent
        if Pos != 0:
            Pos.ispos = 1

    #If the string contanis symbols not defined by the syntax, it is invalid.
    else:
        output = "Invalid:The string contains symbols not defined by the syntax of propositional logic. ({})".format(symbol)
    
    return output,Pos

#The algorithm in question
Trees = []
Pos = 0
with open("Parsing_Input.txt",'r') as f:
    Prop = f.readlines()


for i in range(len(Prop)):
    output = "Valid"
    #Each exercise will be written in a different text file, because some solutions may take up a lot of space.
    f = open("Parsing_Output_{}.txt".format(Prop[i][1]),'w')
    #Prints the letter denoting our current exercise.
    f.write("".join([Prop[i][0],Prop[i][1],Prop[i][2],'\n']))
    #Removes unnecasary characters.
    Prop[i] = Prop[i][4:-2]

    Trees.append(Tree("□"))
    Pos = Trees[i]
    Pos.ispos = 1
    stp = 0

    for j in range(len(Prop[i])):
        symbol = Prop[i][j]

        #In order not to print too much unnnecesary information, blank spaces are skipped, that's why we can't use j as a counter for the steps and need an extra variable.
        if symbol != ' ':
            stp += 1
            f.write("Step {}, Symbol '{}':\n".format(stp,symbol))

            #Separate step for '(' as we need to know if the next symbol is '¬' or another logical connective.
            if symbol == '(':
                if i == len(Prop[i]) - 1:
                    output = "Invalid:The character \'(\' can never be found at the end of a valid propositional formula."

                #Create a child node but don't switch to it as the next step will write '¬' in the current node.
                elif Prop[i][j+1] == '¬':
                    Pos.append('□')

                #Create two child nodes for the two propositions the connective connects and switch to the first one.
                else:
                    Pos.append('□')
                    Pos.append('□')
                    ok = 0
                    for child in Pos.children:
                        if child.name == '□':
                            ok = 1
                            Pos.ispos = 0
                            Pos = child
                            Pos.ispos = 1
                            break
                    if ok == 0 and output == "Valid":
                        output = "Invalid"

            #If we don't have an open paranthesis we can move on to the other cases.
            else:
                output,Pos = step(Pos,symbol)

            #If any problem is detected the algorithm will stop.
            if output != "Valid":
                break
                
            #At each step we show the tree.
            f.write(Trees[i].visualize(0) + '\n')

            #If we exit the tree too early, the string is invalid.
            if Pos == 0 and j != len(Prop[i]) - 1:
                output = "Invalid"
                break

    #Final validation after we exit the tree properly.
    if Trees[i].validate() == False:
        output = "Invalid"

    f.write(output + "\n\n")

f.close()