#Will be used to construct a tree object.
class Tree:
    #Constructor.
    def __init__(self,name):
        self.name = name
        self.children = []
        self.parent = 0
        self.ispos = 0
        self.depth = 0

    #Append a new subtree.
    def append(self,childName):
        Node = Tree(childName)
        Node.parent = self
        Node.depth = self.depth+1
        self.children.append(Node)

    #Returns a string that is a visualization of the tree, along with our position in the tree (if it exists).
    def visualize(self):
        output = "  "*self.depth + self.name + "<--"*self.ispos + '\n'
        for child in self.children:
            output += child.visualize()
        return output

    #Removes all descendents of this node
    def delete_descendents(self):
        self.children = []

    #Used to evaluate the proposition under the interpretations for the propositional variables given by the dictionary v.
    def evaluate(self,v):
        if self.name == '¬':
            return not self.children[0].evaluate(v)
        elif self.name == '∧':
            return self.children[0].evaluate(v) and self.children[1].evaluate(v)
        elif self.name == '∨':
            return self.children[0].evaluate(v) or self.children[1].evaluate(v)
        elif self.name == '⇒':
            return (not self.children[0].evaluate(v)) or self.children[1].evaluate(v)
        elif self.name == '⇔':
            p = self.children[0].evaluate(v)
            q = self.children[1].evaluate(v)
            return (p and q) or ((not p) and (not q))
        else:
            return v[self.name]

    #Returns a list containiing the leaves of the tree that had this node as root, from left to right
    def getLeaves(self):
        Leaves = []
        if self.children == []:
            leaves.append(self.name)
        else:
            for child in self.children:
                child.getLeaves()
        return Leavesdd

