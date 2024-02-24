class Seq:
    def __init__(self, strbases=None):
        if strbases is None:
            print("NULL sequence created")
            self.strbases = "NULL"
        else:
            count = 0
            for e in strbases:
                if e == "A" or e == "C" or e == "G" or e == "T":
                    count += 1
            if count == len(strbases):
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
        else:
            return len(self.strbases)

    def count_base(self, base):
        bases = ["A", "C", "G", "T"]
        for base in bases:
            count = 0
            for i in seq:
                if i == base:
                    count += 1
            print(base, ":", count)

    def count(self):
        dict = {"A": 0, "C": 0, "G": 0, "T": 0}
        count_a = 0
        count_c = 0
        count_g = 0
        count_t = 0
        for i in self.strbases:
            if i == "A":
                count_a += 1
            if i == "T":
                count_t += 1
            if i == "G":
                count_g += 1
            if i == "C":
                count_c += 1
        dict["A"] = count_a
        dict["C"] = count_c
        dict["G"] = count_g
        dict["T"] = count_t
        return dict

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

def generate_seqs(pattern, number):
    list = []
    for i in range(1, number + 1):
        list.append(Seq(pattern * i))
    return list


def print_seqs(seq_list):
    n = 1
    for seq in seq_list:
        print(f"Sequence", n, ": (Length:", seq.len(), ")", seq)
        n += 1
def seq_len(seq):
    seq.len()
def count_seq(seq):
    print("Bases:", seq.count())

def rev_seq(seq):
    print("Rev:", seq.reverse())