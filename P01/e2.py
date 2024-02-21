DNA_BASES = ["A", "T", "C", "G"]


def print_seqs(seq_list):
    n = 0
    for seq in seq_list:
        print(f"Sequence {n} : (Length: {len(seq)}) {seq} \n")
        n += 1


def generate_seqs(pattern, number):
    seq_list = []
    seq = ""
    for i in range(number):
        seq += pattern
        seq_list.append(Seq(seq))
    return seq_list


class Seq:
    def __init__(self, strbases=None):
        if strbases is None:
            print("NULL sequence created")
            self.strbases = "NULL"
        else:
            count = 0
            for base in DNA_BASES:
                count += strbases.count(base)

            if count == len(strbases):
                self.strbases = strbases
                print("New sequence created!")
            else:
                print("INVALID sequence created")
                self.strbases = "ERROR"


    def __len__(self):
        if self.strbases == "NULL" or self.strbases == "ERROR":
            return 0
        else:
            return len(self.strbases)


    def __str__(self):
        return self.strbases


# -- Creating a Null sequence
s1 = Seq()
# -- Creating a valid sequence
s2 = Seq("TATAC")
print(f"Sequence 1: {s1}")
print(f"Sequence 2: {s2}")
