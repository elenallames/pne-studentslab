# Exercise 4
from seq import Seq
import termcolor

def generate_seqs(pattern, number):
    seq_list = []
    for i in range(1, number + 1):
        s = Seq(pattern * i)
        seq_list.append(s)
    return seq_list


def print_seqs(seq_list, color):
    for i, s in enumerate(seq_list):
        termcolor.cprint(f"Sequence {i}: (Length: {s.len()}) {s}", color)


seq_list1 = generate_seqs("A", 3)
seq_list2 = generate_seqs("AC", 5)

termcolor.cprint("List 1:", "blue")
print_seqs(seq_list1, "blue")

print()
print("List 2:", "green")
print_seqs(seq_list2, "green")
