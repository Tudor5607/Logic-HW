import copy

class clause:
    d = {}

    def __init__(self,nr):
        self.disnr = "({})".format(nr)
        self.nr = nr
        self.prime = 0
        self.set = set()

    def __str__(self):
        d = self.d
        if d.get(self.nr,0) == 0:
            return "$" + self.disnr + ' ' + r"\{" + ", ".join(lit_tex(l) for l in self.set) + r"\}$" + r"\\" + '\n'
        else:
            return "$" + self.disnr + ' ' + r"\{" + ", ".join(lit_tex(l) for l in self.set) + r"\}$" + r" from ${}$ and ${}$ \\".format(d[self.nr][0],d[self.nr][1]) + '\n'

    def remove(self,x):
        self.set = self.set.difference({x})
        self.prime += 1
        if self.prime < 5:
            self.disnr = "({}^".format(self.nr) + "{" + '\''*self.prime + "})" 
        else:
            self.disnr = "({}^".format(self.nr) + "{" + "({})".format(self.prime) + "})" 

def lit_tex(lit):
    output  = ''
    if lit[0] == 0:
        output += r"\lnot "
    if len(lit[1]) > 1:
        aux = lit[1][0] + "_{" + lit[1][1:] + '}'
    else:
        aux = lit[1]

    output += aux
    return output

def DPLL(K,set_nr):
    global I,cl_set_nr,impact,cl_nr
    satisfiable = 1
    split = False

    f.write(r"$\mathcal{K}_{" + "{}".format(set_nr) + r"}:$ \\" + '\n')
    f.write("".join(str(C) for C in K) +  r'\\' + '\n')

    while satisfiable == 1 and len(K) > 0:
        one_lit = 0
        pure_lit = 0
        imp_lit = 0
        onr = -1

        #Find the one literal if it exists
        for C in K:
            if len(C.set) == 1:
                x = next(iter(C.set))
                if one_lit == 0 or impact[x[1]][0] + impact[x[1]][1] > impact[one_lit[1]][0] + impact[one_lit[1]][1]:
                    one_lit = x
                    onr = C.disnr

        #Find the pure literal if it exists and the most impactful literal
        for lit in impact.keys():
            tot = impact[lit][0] + impact[lit][1]
            if (impact[lit][0] == 0 and impact[lit][1] != 0) or (impact[lit][1] == 0 and impact[lit][0] != 0):
                if pure_lit == 0 or tot > impact[pure_lit[1]][0] + impact[pure_lit[1]][1]:
                    if impact[lit][0] != 0:
                        pure_lit = (0,lit)
                    else:
                        pure_lit = (1,lit)
            elif imp_lit == 0 or tot > impact[imp_lit][0] + impact[imp_lit][1]:
                imp_lit = lit

        if one_lit != 0:
            I[one_lit[1]] = one_lit[0]
            deleted = []
            removed = []
            comp = (1-one_lit[0],one_lit[1])
            aux = []
            for C in K:
                if one_lit in C.set:
                    deleted.append(C.disnr)
                    for lit in C.set:
                        impact[lit[1]][lit[0]] -= 1
                elif comp in C.set:
                    removed.append(C.disnr)
                    impact[one_lit[1]][1 - one_lit[0]] -=1
                    c = copy.deepcopy(C)
                    c.remove(comp)
                    aux.append(c)
                    if len(c.set) == 0:
                        satisfiable = 0
                else:
                    aux.append(C)
            f.write("We apply the one literal rule for clause ${}$:".format(onr) + r" \\" + '\n')
            f.write("-delete: " + ", ".join(['$' + x + '$' for x in deleted]) + r" \\" + '\n')
            if removed != []:
                f.write("-delete $" + lit_tex(comp) + "$ from " + ", ".join(['$' + x + '$' for x in removed]) + r" \\" + '\n')
            f.write(r"$\mathcal{K}_{" + "{}".format(set_nr) + r"}:$ \\" + '\n')
            K = aux
            f.write("".join(str(C) for C in K) + r'\\' + '\n')
            continue

        elif pure_lit != 0:
            I[pure_lit[1]] = pure_lit[0]
            deleted = []
            aux = []
            for C in K:
                if pure_lit in C.set:
                    deleted.append(C.disnr)
                    for lit in C.set:
                        impact[lit[1]][lit[0]] -= 1
                else:
                    aux.append(C)
            f.write("We apply the pure literal rule for the literal ${}$:".format(lit_tex(pure_lit)) + r" \\" + '\n')
            f.write("-delete: " + ", ".join(['$' + x + '$' for x in deleted]) + r" \\" + '\n')
            f.write(r"$\mathcal{K}_{" + "{}".format(set_nr) + r"}:$ \\" + '\n')
            K = aux
            f.write("".join(str(C) for C in K) + r'\\' + '\n')
            continue

        else:
            split = True
            f.write("We split on the literal " + '$' + lit_tex((1,imp_lit)) + '$' + r" \\ \\" + "\n\n")
            f.write(r"$\mathcal{K}_{" + "{}".format(cl_set_nr + 1) + r"} =\mathcal{K}_{" +"{}".format(set_nr) + r"} \cup \{\{" + lit_tex((1,imp_lit)) + r" \}\}$ \\" + '\n')
            f.write(r"$\mathcal{K}_{" + "{}".format(cl_set_nr + 2) + r"} =\mathcal{K}_{" +"{}".format(set_nr) + r"} \cup \{\{" + lit_tex((0,imp_lit)) + r" \}\}$ \\ \\" + "\n\n")

            n1 = cl_set_nr + 1
            n2 = cl_set_nr + 2
            cl_set_nr += 2
            cl_nr += 1
            c_copy = cl_nr

            save = copy.deepcopy(impact)

            K1 = copy.deepcopy(K)
            aux = clause(c_copy)
            aux.set.add((1,imp_lit))
            impact[imp_lit][1] += 1
            K1.append(aux)
            satisfiable = DPLL(K1,n1)

            if satisfiable == 0:
                impact = save

                K2 = copy.deepcopy(K)
                aux = clause(c_copy)
                aux.set.add((0,imp_lit))
                impact[imp_lit][0] += 1
                K2.append(aux)
                satisfiable = DPLL(K2,n2)
            break

    if not split:
        if satisfiable == 1:
            f.write(r"Satisfiable \\" + "\n\n")
        else:
            f.write(r"Unsatisfiable \\" + "\n\n")

    return satisfiable

        

with open("DPLL_In.txt", 'r', encoding="UTF-8") as f:
    inpt = f.readline().strip(" ,").split('}')[:-1]
inpt = [k.strip("{ ,").split(',') for k in inpt]
inpt = [[v.strip() for v in k] for k in inpt]

f = open("DPLL_Out.txt", 'w', encoding="UTF-8")

impact = {}
K = []
for i in range(len(inpt)):
    s = clause(i + 1)
    k = inpt[i]
    for v in k:
        if v[0] == '¬':
            s.set.add((0,v[1:]))
            if impact.get(v[1:],0) == 0:
                impact[v[1:]] = [0,0]
                impact[v[1:]][0] = 1
            else:
                impact[v[1:]][0] += 1
        else:
            s.set.add((1,v))
            if impact.get(v,0) == 0:
                impact[v] = [0,0]
                impact[v][1] = 1
            else:
                impact[v][1] += 1

    K.append(s)

I = {}
cl_set_nr = 0
cl_nr = len(K)
sat = DPLL(K,0)

for x in impact.keys():
    if x not in I.keys():
        I[x] = 1

if sat == 1:
    I = {x : I[x] for x in sorted(I.keys())}
    f.write(r"So $\mathcal{K}^*_0$ is satisfiable \\" + '\n')
    f.write(r"$\mathcal{I}= \{" + ", ".join([lit_tex((I[x],x)) for x in I.keys()]) + r"\}$ \\" + '\n')
else:
    f.write(r"So $\mathcal{K}^*_0$ is unsatisfiable \\" + '\n')

f.close()