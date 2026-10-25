from HW_AUX.AUXFunctions import *
#Returns a string containing the entire evaluation process of the proposition Prop under interpretation I.
def interpret(Prop,I):
    I = createInterpretation(I)
    T,depth = createAbstractSyntax(Prop)
    yield T.visualize()
    for i in range(depth+1):
        evaluate(T,depth-i,I)
        yield T.visualize()

with open(r"HW2_P6_Truth_values/Interpretation_Input.txt",'r') as f:
    Prop = f.readlines()


f = open(r"HW2_P6_Truth_values/Interpretation_Output.txt",'w')
i = 0
l = len(Prop)
d = {"True":"satisfiable","False":"invalid"}
f.write("Given that we only compute the truth value of each proposition under a single interpretation\nand for any propositional formula with n>0 propositional variables we have 2^n interpretations,\nwe cannot say anything about the validity or nonsatisfiability of these formulas,\nas for these properties we need to check all interpretations.\n\n")
while i < l:
    
    
    #Prints the letter denoting our current exercise.
    f.write("".join([Prop[i][0],Prop[i][1],Prop[i][2],Prop[i+1],'\n']))

    #Removes unnecasary characters.
    Prop[i] = Prop[i][4:]
    interpret(Prop[i],Prop[i+1])

    #Prints the full process of evaluation.
    for step in interpret(Prop[i],Prop[i+1]):
        f.write(step+'\n')
        if step == "True\n" or step == "False\n":
            finalValue = step.strip('\n')
    f.write("Because for this specific interpretation the formula evaluates to {}, we can say the formula is {}.\n\n".format(finalValue,d[finalValue]))
    i += 2

f.close()