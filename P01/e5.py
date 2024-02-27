# Exercise 5

from seq import Seq

PRACTICE = 1
EXCERCISE = 5

print(f"-----| Practice {PRACTICE}, Exercise {EXCERCISE} |------")
seq_list = [Seq(), Seq("ACTGA"), Seq("Invalid sequence")]
for i, s in enumerate(seq_list):
    print(f"Sequence {i + 1}: (Length: {s.len()}) {s}")
    for b in ['A', 'T', 'C', 'G']:
        print(f"\t{b}: {s.count_base(b)}", end="")
    print()
