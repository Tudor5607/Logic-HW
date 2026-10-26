#Generates all possible interpretations for the list of variables "vars" by using the method of binary counting.
def generateInterpretations(vars):
    I = {}
    for var in vars:
        I[var] = "False"
    yield I
    for i in range(2**len(li)-1):
        for var in vars:
            if I[var] == "False":
                I[var] = "True"
                yield I
                break
            else:
                I[var] = "False"