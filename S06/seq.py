def are_bases_ok(strbases):
    ok = True
    for c in strbases:
        if c not in Seq.BASES:
            ok = False
            break
    return ok


class Seq:
    """A class for representing genes"""
    BASES = ['A', 'T', 'C', 'G']

    def __init__(self, strbases):
        if are_bases_ok(strbases):
            self.strbases = strbases
            print("New sequence created!")
        else:
            self.strbases = "ERROR"
            print("INCORRECT Sequence detected")

    def __str__(self):
        return self.strbases

    def len(self):
        return len(self.strbases)


class Gene(Seq):
    """This class is derived from the Seq Class
           All the objects of class Gene will inherit
           the methods from the Seq class
        """

    def __init__(self, strbases, name=""):
        super().__init__(strbases)
        self.name = name
        print("New gene created")

    def __str__(self):
        """Print the Gene name along with the sequence"""
        return self.name + "-" + self.strbases
