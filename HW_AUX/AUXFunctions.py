from HW_AUX.Tree import *

#Converts a string representing a truth value to that truth value
def str_to_bool(value):
    if value == "True":
        return True
    return False

#Checks if something is a truth value
def isTruthValue(sth):
    if sth == "True" or sth == "False":
        return True
    return False

#Checks if the symbol is an atomic proposition.
def isAtomic(symbol):
    if (('a' <= symbol and symbol <= 'z') or ('A' <= symbol and symbol <= 'Z')) and (symbol != "True" and symbol != "False"):
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

#The function takes a (valid) propositional formula as input and returns a tree representing the abstract syntax of the proposition, along with the depth of the tree.
def createAbstractSyntax(Pr):
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

#Creates an interpreration for our propositional vairbles, based on our input.
def createInterpretation(inpt):
    v = {}
    inpt = inpt.split()
    for pair in inpt:
        pair.strip(',.')
        if pair[2] == 'T':
            v[pair[0]] = True
        else:
            v[pair[0]] = False
    return v


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