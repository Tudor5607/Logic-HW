from Tree import *
from symbolF import *

#Renames the current node if it is open. If it fails (the node isn't open) the algorithm we will change the state (here named "output") of the tree to invalid.
def rename(Node,newName):
    output = "Valid"
    #If the node we are trying to write in wasn't marked for a logical connective and we have to rename it, it means we have reached a leaf, which will have to be an atomic proposition.
    if Node.name == "\"F\"":
        if isAtomic(newName) == True:
            Node.name = newName
        else:
            output = "Invalid:Expected an atomic proposition here."
    #Otherwise, the node was marked as a logical connective node.
    elif Node.name == "\"□\"":
        if isConnective(newName) == True:
            Node.name = newName
        else:
            output = "Invalid:Expected a logical connective here"
    else:
        output = "Invalid:Current node is not open."
    return output

#Performs one of the steps described in the parsing algorithm depending on the symbol we input.
#We also have to return the variable Pos just in case we switch positions, as anything done to the internal structure of it (and by extention of the original tree) will be changed, but if we change what Pos is "pointing" towards, the function will not do that, and we need to do a reassignment outside the function.
#The step for '(' gets handled separately as we need to know what the symbol after it is in order to perform it correctly.
def step(Pos,symbol):
        
    #Blank space does nothing.
    if symbol == ' ':
        pass
    
    #If the symbol rerpresents an atomic proposition we write it and move up to the parent node.
    if isAtomic(symbol) == True:
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
    
    return Pos,output

#To be used after we exit the tree succesfully in order to determine if there are any open nodes left and if we have exited the tree.
def validate(Node):
    if Node.name == "\"□\"" or Node.name == "\"F\"":
        return "Invalid:Final tree contains open nodes"
    elif Node.ispos == 1:
        return "Invalid:We haven't exited out of the tree"
    for child in Node.children:
        output = child.validate()
        if output != "Valid":
            return output
    return "Valid"

#The function takes a (valid) propositional formula as input and returns a tree representing the abstract syntax of the proposition, along with the maximum depth of the tree and all the steps taken in order to create the tree.
#If the input is not a valid propositional fomrula (in strict syntax), then the program will still return a tree, along with the reason for the algorithm failing.
def parseStrict(Pr):
    T = Tree("□")
    Pos = T
    depth = 0

    for j in range(len(Pr)):
        symbol = Pr[j]

        #Separate step for '(' as we need to know if the next symbol is '¬' or another logical connective.
        if symbol == '(':

            #Create a child node but don't switch to it as the next step will write '¬' in the current node.
            if Pr[j+1] == '¬':
                Pos.append('□')
                if Pos.children[0].depth > depth:
                    depth = Pos.children[0].depth

            #Create two child nodes for the two propositions the connective connects and switch to the first one.
            else:
                Pos.append('□')
                Pos.append('□')
                if Pos.children[0].depth > depth:
                    depth = Pos.children[0].depth
                for child in Pos.children:
                    if child.name == '□':
                        Pos = child
                        break

        #If we don't have an open paranthesis we can move on to the other cases.
        else:
            Pos = step(Pos,symbol)
    return T,depth