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

def DP(K):
    cl_nr = len(K)
    satisfiable = 1
    ended_resolution = False

    while satisfiable == 1 and len(K) > 0 and not ended_resolution:
        one_lit = 0
        pure_lit = 0
        onr = -1
        clause.d = {}

        #Find the one literal if it exists
        for C in K:
            if len(C.set) == 1:
                x = next(iter(C.set))
                if one_lit == 0 or impact[x[1]][0] + impact[x[1]][1] > impact[one_lit[1]][0] + impact[one_lit[1]][1]:
                    one_lit = x
                    onr = C.disnr

        #Find the pure literal if it exists
        for lit in impact.keys():
            if (impact[lit][0] == 0 and impact[lit][1] != 0) or (impact[lit][1] == 0 and impact[lit][0] != 0):
                tot = impact[lit][0] + impact[lit][1]
                if pure_lit == 0 or tot > impact[pure_lit[1]][0] + impact[pure_lit[1]][1]:
                    if impact[lit][0] != 0:
                        pure_lit = (0,lit)
                    else:
                        pure_lit = (1,lit)

        if one_lit != 0:
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
            f.write(r"The current clause set becomes: \\" + '\n')
            K = aux
            f.write("".join(str(C) for C in K) + r'\\' + '\n')
            continue

        elif pure_lit != 0:
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
            f.write(r"The current clause set becomes: \\" + '\n')
            K = aux
            f.write("".join(str(C) for C in K) + r'\\' + '\n')
            continue

        else:
            vars = [x for x in impact.keys() if impact[x] != [0,0]]
            i = 0
            l = len(K)
            A = sorted(K,key=lambda x : len(x.set))
            found_unit = 0
            while i < l and satisfiable == 1 and found_unit == 0:
                for s in A[i].set:
                    for j in range(l):
                        if i != j and (1-s[0],s[1]) in A[j].set:
                            u = A[i].set.union(A[j].set)
                            u = u.difference({(0, s[1]), (1, s[1])})

                            good = 1
                            for let in vars:
                                if (0,let) in u and (1,let) in u:
                                    good = 0
                                    break

                            if u not in [C.set for C in K] and good == 1:
                                cl_nr += 1
                                ua = clause(cl_nr)
                                ua.set = u
                                clause.d[ua.nr] = [A[i].disnr,A[j].disnr]
                                K.append(ua)
                                A.append(ua)
                                for lit in ua.set:
                                    impact[lit[1]][lit[0]] += 1
                                l = len(K)

                            if u == set():
                                satisfiable = 0
                                break

                            if len(u) == 1:
                                found_unit = 1
                                break
                    
                    if found_unit == 1 or satisfiable == 0:
                        break
                i += 1

            if i == l:
                ended_resolution = True
                f.write("We apply resolution and in this case it finishes" + r" \\" + '\n')
                f.write(r"The final clause set becomes: \\" + '\n')
                f.write("".join(str(C) for C in K) + r'\\' + '\n')

            elif satisfiable == 0:
                ended_resolution = True
                f.write("We apply resolution and in this case we obtain the empty clause" + r" \\" + '\n')
                f.write(r"The final clause set becomes: \\" + '\n')
                f.write("".join(str(C) for C in K) + r'\\' + '\n')

            else:
                f.write("We apply resolution until we are able to apply the one literal rule" + r" \\" + '\n')
                f.write(r"The current clause set becomes: \\" + '\n')
                f.write("".join(str(C) for C in K) + r'\\' + '\n')

    return satisfiable

        

with open("DP_In.txt", 'r', encoding="UTF-8") as f:
    inpt = f.readline().strip(" ,").split('}')[:-1]
inpt = [k.strip("{ ,").split(',') for k in inpt]
inpt = [[v.strip() for v in k] for k in inpt]

f = open("DP_Out.txt", 'w', encoding="UTF-8")

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

f.write(r"Initial clause set: \\" + '\n')
f.write("".join(str(C) for C in K) +  r'\\' + '\n')

sat = DP(K)
if sat == 1:
    f.write(r"Satisfiable \\" + '\n')
else:
    f.write(r"Unsatisfiable \\" + '\n')


f.close()