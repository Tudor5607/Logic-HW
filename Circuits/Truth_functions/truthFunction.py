formula = ""
formula_tex = ""


with open("truthFunction_In.txt",'r') as f:

    n = int(f.readline())
    vars = f.readline()
    vars = vars.split()
    negated = {'T':0, 'F':1}

    for i in range(2**n):
        line = f.readline()
        line = line[:-1]
        if line[-1] == 'T':
            formula += '('
            formula_tex += '('
            line = line.split()
            for j in range(len(line)-1):
                formula += negated[line[j]]*'¬' + vars[j] + " ∧ "
                formula_tex += negated[line[j]]*r" \lnot" + ' ' + vars[j] + r" \land"

            formula = formula[:-3]
            formula_tex = formula_tex[:-5]

            formula += ") ∨ "
            formula_tex += r") \lor "

formula = formula[:-3]
formula_tex = formula_tex[:-6]

with open("truthFunction_Out.txt",'w') as f:
    f.write(formula_tex + '\n')
    f.write(formula)
