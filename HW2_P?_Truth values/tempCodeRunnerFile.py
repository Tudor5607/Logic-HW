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