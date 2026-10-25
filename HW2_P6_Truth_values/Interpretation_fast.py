from HW_AUX.AUXFunctions import *

#Returns the interpretation of Proposition "Prop" under the interpretation I.
def interpretFast(Prop,I):
    I = createInterpretation(I)
    T,depth = createAbstractSyntax(Prop)
    return str(T.evaluate(I))

if __name__ == "__main__":
    with open(r"HW2_P6_Truth_values/Interpretation_Input_test.txt",'r') as f:
        Prop = f.readlines()

    f = open(r"HW2_P6_Truth_values/Interpretation_Output_test.txt",'w')
    i = 0
    l = len(Prop)
    while i < l:
        #Prints the letter denoting our current exercise.
        f.write("".join([Prop[i][0],Prop[i][1],Prop[i][2]," "]))

        #Removes unnecasary characters.
        Prop[i] = Prop[i][4:]

        f.write(interpretFast(Prop[i],Prop[i+1]) + "\n")
        i += 2

    f.close()