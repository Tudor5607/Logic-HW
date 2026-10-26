from Tree import *
from symbolF import *
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