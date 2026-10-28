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

    #Returns a string that is a visualization of the tree in polish notation. (recommended only for complete trees)
    def polish(self):
        output = self.name
        for child in self.children:
            output += child.polish()
        return output

    #To be used after we exit the tree succesfully in order to determine if there are any open nodes left and if we have exited the tree.
    def validate(self):
        if self.name == "\"□\"" or self.name == "\"F\"":
            return "Invalid:Final tree contains open nodes"
        elif self.ispos == 1:
            return "Invalid:We haven't exited out of the tree"
        for child in self.children:
            output = child.validate()
            if output != "No errors":
                return output
        return "No errors"

#Class used solely to define an order on symbols
class Symbol:

    priority = {'⇔':1,'⇒':2,'∨':3,'∧':3,'¬':4}

    def __init__(self,name):
        self.name = name
    
    def __lt__(self,other):
        return self.priority[self.name] < self.priority[other.name]

    def __repr__(self):
        return "".join(["'",self.name,"'"])

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

#Will be used to attempt to create the abstract syntax after the shunting yard algorithm finishes.
def fill(Node):
    global error,Pos,Q,i
    Pos.ispos = 0
    Pos = Node
    Pos.ispos = 1
    f.write("Symbol:{}\n".format(Q[i]))
    f.write(T.visualize()+'\n')
    if isConnective(Q[i]):
        if Q[i] == '¬':
            Pos.name = '¬'
            Pos.append("\"F\"")
            
            i += 1
            fill(Pos.children[0])
        else:
            Pos.name = Q[i]
            Pos.append("\"F\"")
            Pos.append("\"F\"")

            i += 1
            fill(Pos.children[1])
            i += 1
            fill(Pos.children[0])
    else:
        if Node.name == "\"F\"":
            Node.name = Q[i]
        else:
            error = "Invalid:Error when creating abstract syntax, node is not open."
    
    Pos.ispos = 0
    Pos = Node.parent
    if Pos != 0:
        Pos.ispos = 1

with open("parseR_In.txt",'r') as f:
    exps = f.readlines()

f = open("parseR_Out.txt",'w')
for exp in exps:
    error = "No errors"

    f.write("".join([exp[0],exp[1],exp[2],'\n']))
    exp = exp[4:-2]
    Q = []
    S = []

    #We start by expecting either an open parenthesis, a propositional variable or a negation operator, propositions in relaxed syntax cannot start with anything else.
    #Also after any symbol we may expect one out of two sets of symbols, namely ['(','¬',"var"] or expect = [')','∧','∨','⇒','⇔']. We will represent the first set with 0 and the second with 1.
    #d = [['(','¬',"var"],[')','∧','∨','⇒','⇔']]  
    expect = 0
    f.write("Expect:{}\nQueue:{}\nStack:{}\n\n".format(expect,Q,S))
    if exp[-1] != ')' and (not isAtomic(exp[-1])):
        error = "Invalid:A valid proposition may only end with a closed paranthesis or a propositional variable."
    for symb in exp:
        
        if error != "No errors":
            break

        #Spaces are not relevant.
        if symb != ' ':
            f.write("Symbol:'{}'\nExpect:{}\n".format(symb,expect))

            #If the symbol is a propositional variable it gets added to the queue.
            if isAtomic(symb) == True:
                if expect == 0:
                    Q.append(symb)
                    #After a propositional variable we exect either a closed parenthesis or a binary logical connective.
                    expect = 1
                else:
                    error = "Invalid:Expected a different symbol here."

            #For logical connectives we may need to check precedence first.
            elif isConnective(symb):
                if (expect == 1 and symb != '¬') or (expect == 0 and symb == '¬'):
                    A = Symbol(symb)
                    if len(S) == 0 or S[-1] == '(':
                        S.append(A)
                    else:
                        while len(S) != 0 and S[-1] != '(' and A < S[-1]:
                            Q.append(S[-1].name)
                            S.pop()
                        S.append(A)

                    #After a logical connective we expect either an open parenthesis, a propositional variable or a negaton.
                    expect = 0
                else:
                    error = "Invalid:Expected a different symbol here."

            #An open paranthesis doesn't do anything on its own, but has interactions with other steps.
            elif symb == '(':
                if expect == 0:
                    S.append(symb)
                    #After an open paranthesis we expect either another open paranthesis, a propositional variable or a negation.
                else:
                    error = "Invalid:Expected a different symbol here."

            #A closed paranthesis must have an accompanying open paranthesis to determine the priority of connectives.
            elif symb == ')':
                if expect == 1:
                    if S[-1] == '(':
                        error = "Invalid:Unnecessary parentheses"
                    else:
                        while len(S) != 0 and S[-1] != '(':
                            Q.append(S[-1].name)
                            S.pop()
                        if len(S) == 0:
                            error = "Invalid:Proposition contains an unclosed right parenthesis."
                        else:
                            S.pop()
                    #After a closed paranthesis we expect either another closed paranthesis or a binary logical connective.
                else:
                    error = "Invalid:Expected a different symbol here."

            else:
                error = "Invalid:Proposition contains undefined symbols."

            f.write("Queue:{}\nStack:{}\n\n".format(Q,S))

    #We clean the stack after all symbols have ran out.
    if error == "No errors":
        while len(S) != 0 and S[-1] != '(':
            Q.append(S[-1].name)
            S.pop()
        if len(S) != 0:
            f.write("Queue:{}\nStack:{}\n\n".format(Q,S))
            error = "Invalid:Proposition contains an unclosed left parenthesis."

    #We will construct the abstract syntax from the bottom to the top. The current form of the proposition (assuming we got to this point without errors) actually represents the operation priorities.
    if error == "No errors":
        Q.reverse()
        f.write("Queue:{}\nStack:{}\n\n".format(Q,S))

        i = 0
        T = Tree("\"F\"")
        Pos = T
        fill(T)

    #If everything went fine, we can print the abstract syntax..
    if error == "No errors":
        f.write(T.visualize()+'\n')
        f.write(T.polish()+"\n\n")
        f.write("Valid propositional formula in relaxed syntax.\n\n")
    else:
        f.write("".join([error,"\n\n"]))

f.close()