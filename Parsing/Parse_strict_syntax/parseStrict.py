atomic_propositions = []
#A class that we will use in the parsing algorithm.
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
        output = "    "*level + self.name + self.ispos*"<--" + '\n'
        for child in self.children:
            output += child.visualize(level + 1)
        return output

    #Returns a string that is a visualization of the tree in polish notation. (recommended only for complete trees)
    def polish(self):
        output = self.name
        for child in self.children:
            output += child.polish()
        return output

    #Renames the current node if it is open. If it fails (the node isn't open) the algorithm we will change the state (here named "output") of the tree to invalid.
    def rename(self,newName):
        output = "Valid"
        #If the node we are trying to write in wasn't marked for a logical connective and we have to rename it, it means we have reached a leaf, which will have to be an atomic proposition.
        if self.name == "\"F\"":
            if isAtomic(newName) == True:
                self.name = newName
            else:
                output = "Invalid:Expected an atomic proposition here."
        #Otherwise, the node was marked as a logical connective node.
        elif self.name == "\"□\"":
            if isConnective(newName) == True:
                self.name = newName
            else:
                output = "Invalid:Expected a logical connective here"
        else:
            output = "Invalid:Current node is not open."
        return output

    #To be used after we exit the tree succesfully in order to determine if there are any open nodes left and if we have exited the tree.
    def validate(self):
        if self.name == "\"□\"" or self.name == "\"F\"":
            return "Invalid:Final tree contains open nodes"
        elif self.ispos == 1:
            return "Invalid:We haven't exited out of the tree"
        for child in self.children:
            output = child.validate()
            if output != "Valid":
                return output
        return "Valid"


#Some auxiliary functions.

#Checks if the symbol is a letter, which means we have reached an atomic propositon.
def isAtomic(symbol):
    if ( (('a' <= symbol <= 'z') or ('A' <= symbol <= 'Z')) and len(symbol) == 1) or symbol == '⊤' or symbol == '⊥':
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
        if output == "Valid":
            Pos.ispos = 0
            Pos = Pos.parent
            if Pos != 0:
                Pos.ispos = 1

    #Logical connectives get written and move down to the first available child of the node.
    elif isConnective(symbol) == True:
        output = Pos.rename(symbol)
        if output == "Valid":
            ok = 0
            for child in Pos.children:
                if child.name == "\"F\"":
                    ok = 1
                    Pos.ispos = 0
                    Pos = child
                    Pos.ispos = 1
                    break
        #If the node doesn't have any open subtree nodes but we need to move to one something went wrong.
            if ok == 0:
                output = "Invalid:We need to move to and open subtree node, but there are none to move to."

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

#The parsing algorithm
Trees = []
Pos = 0
with open("parseS_In.txt",'r', encoding="UTF-8") as f:
    Prop = f.readlines()

f = open("parseS_Out.txt",'w', encoding="UTF-8")
f.write("Note: This solution was written with the help of an algorithm. Because of that I have used a \"folder\" notation for the tree in order to make it easier to print.\n\n")
for i in range(len(Prop)):
    output = "Valid"

    #We write the proposition we are trying to parse
    f.write(Prop[i] + '\n')

    #We remove the newline character at the end
    Prop[i] = Prop[i][:-1]

    Trees.append(Tree("\"F\""))
    Pos = Trees[i]
    Pos.ispos = 1
    stp = 0

    for j in range(len(Prop[i])):
        symbol = Prop[i][j]

        #In order not to print too much unnnecesary information, blank spaces are skipped, that's why we can't use j as a counter for the steps and need an extra variable.
        if symbol != ' ':
            stp += 1
            #The outputs are written in separate text files.
            f.write("Step {}, Symbol '{}':\n".format(stp,symbol))

            #Separate step for '(' as we need to know if the next symbol is '¬' or another logical connective.
            if symbol == '(':
                Pos.name = "\"□\""
                if j == len(Prop[i]) - 1:
                    output = "Invalid:The character \'(\' can never be found at the end of a valid propositional formula."

                #Create an open subtree node but don't switch to it as the next step will write '¬' in the current node.
                #If the appending would lead to more than one child for the current node we know something went wrong.
                elif Prop[i][j+1] == '¬':
                    if Pos.children != []:
                        output = "Invalid:The next step would print the '¬' connective here, but the structure of the subtree wouldn't be correct in that case."
                    Pos.append("\"F\"")

                #Create two open subtree nodes for the two propositions the connective will connect and switch to the first one.
                #If the appending would lead to more than 2 children for the current node we know something went wrong.
                else:
                    if Pos.children != []:
                        output = "Invalid:A node may have at most 2 children."
                    Pos.append("\"F\"")
                    Pos.append("\"F\"")
                    for child in Pos.children:
                        if child.name == "\"F\"":
                            Pos.ispos = 0
                            Pos = child
                            Pos.ispos = 1
                            break

            #If we don't have an open paranthesis we can move on to the other cases.
            else:
                output,Pos = step(Pos,symbol)
                
            #At each step we show the tree.
            f.write(Trees[i].visualize(0) + '\n')

            #We must not exit the tree too early.
            if Pos == 0 and j != len(Prop[i]) - 1:
                output = "Invalid:We exited the tree too early."
                break

            #If any problem is detected the algorithm will stop.
            if output != "Valid":
                break

    #If we run out of characters and no problems were detected yet, we need to check if there are any open nodes left and if we have exited the tree.
    if output == "Valid":
        output = Trees[i].validate()

    f.write(output + "\n\n")

    if output == "Valid":
        f.write(Trees[i].polish() + "\n\n")

f.close()