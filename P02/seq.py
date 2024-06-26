def are_bases_ok(strbases):
    return all(c in Seq.BASES for c in strbases)

class Seq:
    """A class for representing genes"""
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
        return len(self.strbases) if self.strbases not in {"NULL", "ERROR"} else 0

    def count_base(self, base):
        return self.strbases.count(base) if self.strbases not in {"NULL", "ERROR"} else 0

    def count(self):
        return {base: self.count_base(base) for base in Seq.BASES}

    def reverse(self):
        return self.strbases[::-1] if self.strbases not in {"NULL", "ERROR"} else "ERROR"

    def complement(self):
        if self.strbases in {"NULL", "ERROR"}:
            return "ERROR"
        complement_map = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
        return ''.join(complement_map.get(base, "ERROR") for base in self.strbases)

    def read_fasta(self, filename):
        from pathlib import Path

        file_content = Path(filename).read_text()
        lines = file_content.splitlines()
        self.strbases = ''.join(lines[1:])

    def max_base(self):
        counts = self.count()
        return max(counts, key=counts.get)

    def info(self):
        print(f"Sequence: {self.strbases}")
        print(f"Length: {self.len()}")
        print(f"Base counts: {self.count()}")
        print(f"Reverse: {self.reverse()}")
        print(f"Complement: {self.complement()}")
        print(f"Most frequent base: {self.max_base()}")

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
        return f"{self.name}-{self.strbases}"