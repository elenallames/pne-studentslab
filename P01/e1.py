class Seq:
    def __init__(self, strbases):
        count = 0
        for e in strbases:
            if e == "A":
                count += 1
            if e == "C":
                count += 1
            if e == "G":
                count += 1
            if e == "T":
                count += 1
        if count == len(strbases):
            self.strbases = strbases
            print("New sequence created!")

    def __str__(self):
        return self.strbases
    def len(self):
        return len(self.strbases)

def print_seqs(seq_list):
    n = 0
    for seq in seq_list:
        print(f"Sequence", n, ": (Length:", seq.len(), ")", seq)
        n += 1

seq_list = [Seq("ACTGA")]
print_seqs(seq_list)

