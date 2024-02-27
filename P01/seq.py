def are_bases_ok(strbases):
    ok = True
    for c in strbases:
        if c not in Seq.BASES:
            ok = False
            break
    return ok


class Seq:
    """A class for representing sequences"""
    BASES = ['A', 'T', 'C', 'G']

    def __init__(self, strbases=None):
        if strbases is None:
            self.strbases = "NULL"
            print("NULL sequence created")
        elif are_bases_ok(strbases):
            self.strbases = strbases
            print("New sequence created!")
        else:
            self.strbases = "ERROR"
            print("INVALID sequence!")

    def __str__(self):
        return self.strbases

    def len(self):
        if self.strbases == "NULL" or self.strbases == "ERROR":
            return 0
        return len(self.strbases)

    def count_base(self, base):
        if self.strbases == "NULL" or self.strbases == "ERROR":
            return 0
        return self.strbases.count(base)

    def count(self):
        bases_appearances = {}
        for base in Seq.BASES:
            bases_appearances[base] = self.count_base(base)
        return bases_appearances

    def reverse(self):
        if self.strbases == "NULL" or self.strbases == "ERROR":
            return "ERROR"
        else:
            reverse = ''
            seq = self.strbases
            index = len(seq) - 1
            while index >= 0:
                reverse += seq[index]
                index -= 1
            return reverse

    def complement(self):
        complement = ""
        if self.strbases is None:
            return "NULL"
        else:
            for base in self.strbases:
                if base == "A":
                    complement += "T"
                elif base == "G":
                    complement += "C"
                elif base == "C":
                    complement += "G"
                elif base == "T":
                    complement += "A"
                else:
                    return "ERROR"
        return complement


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
