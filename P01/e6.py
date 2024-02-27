# Exercise 6

from seq import Seq

PRACTICE = 1
EXCERCISE = 6

print(f"-----| Practice {PRACTICE}, Exercise {EXCERCISE} |------")
seq_list = [Seq(), Seq("ACTGA"), Seq("Invalid sequence")]
for i, s in enumerate(seq_list):
    print(f"Sequence {i + 1}: (Length: {s.len()}) {s}")
    print(f"\tBases: {s.count()}")