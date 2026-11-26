with open("Resolution_In.txt", 'r' , encoding="UTF-8") as f:
    K = f.readline()

K = K.strip(" ,")
K = K.split('}')
K.pop()
K = [k.strip("{ ,").split(',') for k in K]
K = [[v.strip() for v in k] for k in K]
letters = []
vars = []


for k in K:
    s = set()
    for v in k:
        if v[0] == '¬':
            s.add((0,v[1:]))
            if v[1] not in letters:
                letters.append(v[1])
        else:
            s.add((1,v))
            if v not in letters:
                letters.append(v)
    vars.append([s,-1,-1])

f = open("Resolution_Out.txt", 'w' , encoding="UTF-8")

i = 0
l = len(vars)

end = 0
while i < l:
    for s in vars[i][0]:
        for j in range(l):
            if i != j and (1-s[0],s[1]) in vars[j][0]:
                u = vars[i][0].union(vars[j][0])
                u = u.difference({(0, s[1]), (1, s[1])})

                good = 1
                for let in letters:
                    if (0,let) in u and (1,let) in u:
                        good = 0
                        break

                if u == set():
                    end = 1

                if u not in [a[0] for a in vars] and good == 1:
                    vars.append([u,i+1,j+1])
                l = len(vars)

            if end == 1:
                break

        if end == 1:
            break
    i += 1
    if end == 1:
        break

for i in range(len(vars)):
    v = vars[i]
    s = v[0]
    aux = []
    for u in s:
        tex = u[1]
        if len(tex) > 1:
            tex = tex[0] + "_{" + tex[1:] + '}'
        if u[0] == 0:
            tex = r"\lnot " + tex
        aux.append(tex)

    if v[1] == -1:
        f.write("({}) $".format(i+1) + r"\{" + ", ".join(aux) + r" \}" + r"$ \\" + '\n')
    else:
        f.write("({}) $".format(i+1) + r"\{" + ", ".join(aux) + r" \}"  + r"$ from ({}) and ({})\\".format(v[1],v[2]) + '\n')

if end == 1:
    f.write("\n" + "Unsatisfiable")
else:
    f.write("\n"+"Satisfiable")

f.close()