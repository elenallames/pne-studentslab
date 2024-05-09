"""This file is our module, that will be imported in all the exercises"""

# STRBASES is a string that will be stored in every object of class Seq that we use to represent a sequence


def valid_bases(strbases):
    valid = True
    for b in strbases:
        if b not in Seq.BASES:  # the Seq in front indicates that bases_list is a class attribute
            valid = False
            break  # you exit the for loop, but not the entire function
    return valid


class Seq:
    BASES = ["A", "C", "T", "G"]  # list with the bases of a DNA sequence (class attribute or property or static)
    COMPLEMENTS = {"A": "T", "T": "A", "C": "G", "G": "C"}  # dictionary with complement base of each of the og bases

    def __init__(self, strbases=None):
        if strbases is None or len(strbases) == 0:  # the same as strbases == 0 --> empty
            self.strbases = "NULL"
            print("NULL sequence created")
        elif valid_bases(strbases):  # if the seq/strbases contains the same bases as in BASES, then it is VALID
            self.strbases = strbases
            print("New sequence created!")
        else:  # if it is not VALID, and it is not NULL, then it is INCORRECT/INVALID
            self.strbases = "ERROR"
            print("INVALID sequence!")

    def __str__(self):
        return self.strbases

    def len(self):
        if self.strbases == "NULL" or self.strbases == "ERROR":
            length = 0
            # return 0
        # return len(self.strbases)
        else:
            length = len(self.strbases)
        return length

    def count_base(self, base):
        if self.strbases == "NULL" or self.strbases == "ERROR":
            count = 0
            # return 0
        # return self.strbases.count(base)
        else:
            count = self.strbases.count(base)
        return count

    def count(self):  # as we use count_base, in this function we don't need to check if the sequence is valid
        bases_dict = {}

        for b in Seq.BASES:  # b acting as each one of the bases of our list of valid bases(class property BASES)
            bases_dict[b] = self.count_base(b)  # the value of each one of the keys(b) will be their individual count
        return bases_dict

    def reverse(self):
        if self.strbases == "NULL":
            reverse = "NULL"
        elif self.strbases == "ERROR":
            reverse = "ERROR"
        else:
            reverse = self.strbases[::-1]
        return reverse

    def complement(self):
        if self.strbases == "NULL":
            complementary_seq = "NULL"
        elif self.strbases == "ERROR":
            complementary_seq = "ERROR"
        else:
            complementary_seq = ""
            for b in self.strbases:
                complementary_seq += Seq.COMPLEMENTS[b]
        return complementary_seq

    def read_fasta(self, filename):
        from pathlib import Path

        file_content = Path(filename).read_text()
        lines = file_content.splitlines()
        body = lines[1:]
        # "".join(body) is the same as the following for loop
        self.strbases = ""
        for line in body:
            self.strbases += line  # dna_sequence = dna_sequence + line

    def max_base(self):
        if self.strbases == "NULL" or self.strbases == "ERROR":
            return None
        max_base = ""
        max_count = 0
        for base in Seq.BASES:
            count = self.count_base(base)
            if count > max_count:
                max_count = count
                max_base = base
        return max_base

    def info(self):
        s = f"Total length: {self.len()}\n"
        for base in Seq.BASES:
            if self.len() == 0:  # we discard the invalid and null sequences
                percentage = 0
            else:
                percentage = round((self.count_base(base) * 100) / self.len(), 1)
            s += f"{base}: {self.count_base(base)} ({percentage}%)\n"

        return s

    """ANOTHER WAY TO DO IT IS USING THE METHOD COUNT():  base=key and count=value in our dictionary (self.count())
    s = f"Total length: {self.len()}\n"
    for base, count in self.count().items():  # we iterate over the items of our dict
        if self.len() == 0 :
            percentage = 0
        else:
            percentage = (count * 100) / self.len()
        s += f"{base}: {count} ({percentage:.1f}%)\n"  # :.1f TAKES THE PERCENTAGE WITH FORMAT OF ONE DECIMAL
    return s
    """