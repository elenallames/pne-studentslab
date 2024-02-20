#exercise 3
class Seq:
    def __init__(self, strbases):
        self.strbases = strbases
        print("New list created!")

    def __str__(self):
        return self.strbases

    def len(self):
        return len(self.strbases)

def generate_seqs(pattern, number):
    list = []
    for i in range(1, number + 1):
        list.append(Seq(pattern * i))
    return list

def print_seqs(seq_list):
    n = 0
    for seq in seq_list:
        print(f"Sequence", n, ": (Length:", seq.len(), ")", seq)
        n += 1

seq_list1 = generate_seqs("A", 3)
seq_list2 = generate_seqs("AC", 5)

print("List 1:")
print_seqs(seq_list1)

print()
print("List 2:")
print_seqs(seq_list2)
