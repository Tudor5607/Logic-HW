#An implementatio of the Quine–McCluskey algorithm that shows the steps we need to take in order to reach the result.
#Will be used to construct a tree object.
class Tree:
    #Constructor.
    def __init__(self,name):
        self.name = name
        self.children = []
        self.parent = 0
        self.depth = 0

    def __repr__(self):
        return str([self.name,self.children])

    #Append a new subtree.
    def append(self,childName):
        Node = Tree(childName)
        Node.parent = self
        Node.depth = self.depth+1
        self.children.append(Node)

    #Returns a list containiing the leaves of the tree that had this node as root, from left to right
    def getLeaves(self):
        Leaves = []
        if self.children == []:
            Leaves.append(self.name)
        else:
            for child in self.children:
                Leaves.extend(child.getLeaves())
        return Leaves

#Converts an expression containig special logical characters into one compatible with latex
def lateXfy(str):
    str = str.replace('¬',r"\lnot ")
    str = str.replace('∧',r"\land")
    str = str.replace('∨',r"\lor")
    return str

#Returns the number of ones in a term representinig a conjunction of negations and non-negations of atomic propositions.
def get_ones(component):
    s = 0
    for bit in component:
        if bit == '1':
            s += 1
    return s

#Tells us if we can combine to terms in order to simplify get rid of a proposition.
def can_combine(a,b):
    diff = 2
    ok = 1

    if get_ones(a) == get_ones(b) - 1:
        for i in range(len(a)):
            if a[i] != b[i]:
                diff -= 1
                if diff < 1:
                    break
            if (a[i] == '-' and b[i] != '-') or (b[i] == '-' and a[i] != '-'):
                ok = 0
                break

    if diff == 1 and ok == 1:
        return True
    return False

#Combines comptabile terms
def combine(a,b):
    s = ""
    for i in range(len(a)):
        if a[i] != b[i]:
            s += '-'
        else:
            s += a[i]
    return s

def get_essentials(terms,es):
    global essential,implicants

    if terms != []:
        v = terms[-1].name
        for k in implicants[v]:
            temp  = terms[:]
            es.append(k)

            for u in terms:
                if k in implicants[u.name]:
                    temp.remove(u)

            temp.sort(key = lambda x : len(implicants[x.name]),reverse=True)
            get_essentials(temp,es)

            es.pop()
    else:
        if len(es) < len(essential):
            essential = es[:]

#Used to explicitly write all the steps we needed to get to the solution
def write_steps(ok):
    global steps
    if ok == 1:
        ok = 0
        t = []
        for x in steps[-1]:
            if x.children != []:
                ok = 1
                t.extend([x.children[0]])
                t.extend([x.children[1]])
            else:
                t.append(x)
        steps.append(t)
        write_steps(ok)
    else:
        steps.pop()


with open("simplification_In.txt",'r',encoding="UTF-8") as f:
    exp = f.readline().strip("\n ")

f = open("simplification_Out.txt",'w',encoding="UTF-8")
f.write(lateXfy(exp))

exp = exp.split(" ∨ ")
#vars will store the variables we have in the order that they appear in the expressions containig conjunctions, and their indices.
vars = {}
#terms will store a set of terms that represent each term containing conjunction, it will have a 0 of the proposition is negated and 1 otherwise.
terms = []

#First we find all the variables present in the expressions.
i = 0
for sub in exp:
    sub = sub.strip("()")
    sub = sub.split(" ∧ ")
    for var in sub:
        if var[0] == '¬':
            if var[1:] not in vars:
                vars[var[1:]] = i
                i += 1
        else:
            if var not in vars:
                vars[var] = i
                i += 1

#Converts the expression into a simpler seqence of 0s, 1s and possibly -s in case a variable does not appear in the expression.
for sub in exp:
    terms.append(['-']*len(vars))
    sub = sub.strip("()")
    sub = sub.split(" ∧ ")
    for var in sub:
        if var[0] == '¬':
            terms[-1][vars[var[1:]]] = '0'
        else:
            terms[-1][vars[var]] = '1'

#Converts the list of lists into a list of strings, also in case there are dashed lines in the original, additional terms are added in order to make sure each term has all variables and the algorithm runs properly.
temp = []
for term in terms:
    x = [""]
    for nr in term:
        if nr == '-':
            t = []
            for i in range(len(x)):
                t.append(x[i] + '0')
                t.append(x[i] + '1')
            x = t
        else:
            for i in range(len(x)):
                x[i] += nr
    temp.extend(x)
terms = temp

terms.sort(key= lambda x : get_ones(x))

#A tree will be used in order to remember the elements we need to merge in order to get to our desired result.
terms = [Tree(x) for x in terms]


temp = terms[:]
changes  = -1
while changes != 0:
    #We will remember which terms have been merged and which ones can no longer be merged, so the are "prime".
    merged = [False for x in temp]
    changes = 0
    prime_imp = []

    for i in range(len(temp)):
        for j in range(i+1,len(temp)):
            #We check all possible pairs of terms in order to see if they can be merged.
            m1 = temp[i]
            m2 = temp[j]

            if can_combine(m1.name,m2.name) == True:
                m = combine(m1.name,m2.name)
                merged[i] = True
                merged[j] = True
                changes += 1

                #We will only add new elements, if an element is reached twice, the only thing that will differ is the way we combined elements to get to it, not the actual elements that were combined.
                if m not in [x.name for x in prime_imp]:
                    m = Tree(m)
                    m.children = [m1,m2]
                    prime_imp.append(m)

    #All elements that cannot be combined any further are prime.
    for i in range(len(temp)):
        if merged[i] == False:
            prime_imp.append(temp[i])

    temp = prime_imp

essential = [x for x in prime_imp]
implicants = {x.name:[] for x in terms}

#We assign to each conjunction in the original expression, the simplified expressions that cover it.
for p in prime_imp:
    l = p.getLeaves()
    for exp in l:
        implicants[exp].append(p)

#We start from the term with the least amound of coverings.
terms.sort(key = lambda x : len(implicants[x.name]),reverse=True)

#Once we get the minimal list of essential terms, we need to print out the steps we used to get from the original expression to it.
get_essentials(terms,[])
steps = []
steps.append(essential)
write_steps(1)

#We will reuse the variable vars but in the opposite way
vars = [symb for symb in vars.keys()]

steps.reverse()
steps = [[x.name for x in y] for y in steps]

for s in steps:
    st = []
    for t in s:
        lits = []
        for i in range(len(t)):
            if t[i] == '1':
                lits.append(vars[i])
            elif t[i] == '0':
                lits.append(r"\lnot " + vars[i])
        if lits == []:
            lits = r"\top"
        elif len(lits) == 1:
            lits = lits[0]
        else:
            lits =  "(" + r" \land ".join(lits) + ")"

        st.append(lits)

    f.write(r" \sim " + r" \lor ".join(st))

f.close()