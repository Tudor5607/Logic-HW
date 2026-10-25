from HW_AUX.AUXFunctions import *
from HW_AUX.InterpretationsGenerator import generateInterpretations
from HW2_P6_Truth_values.Interpretation_full import interpret

def establishEquivalence(P0,P1):
    T0,lev1 = createAbstractSyntax(P0)
    T1,lev2 = createAbstractSyntax(P1)
    vars = Set(T0.getLeaves()) + Set(T1.getLeaves())
    print(vars)


with open(r"HW2_P4_Equivalence/equivalence_input.txt",'r') as f:
    Props = f.readlines()

f = open(r"HW2_P4_Equivalence/equivalence_output.txt",'w')
for Prop in Props:
    f.write("".join([Prop[0],Prop[1],Prop[2],'\n']))
    Prop = Prop[4:].strip(".,\n")
    Prop = Prop.split("∼")
    print(Prop)
    print(establishEquivalence(Prop[0],Prop[1]))

f.close()
