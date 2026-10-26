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
    if (('a' <= symbol <= 'z') or ('A' <= symbol <= 'Z')) and (symbol != "True" and symbol != "False"):
        return True
    return False

#Checks if the symbol is a logical connective.
def isConnective(symbol):
    if symbol == '¬' or symbol == '∧' or symbol == '∨' or symbol == '⇒' or symbol == '⇔':
        return True
    return False

#Creates an interpreration for our propositional vairbles, based on our input.
def createInterpretation(inpt):
    v = {}
    inpt = inpt.split()
    for pair in inpt:
        pair.strip(',.')
        if pair[2] == 'T':
            v[pair[0]] = "True"
        else:
            v[pair[0]] = "False"
    return v
