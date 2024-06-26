# Exercise 8
from seq import Seq

PRACTICE = 1
EXCERCISE = 8

print(f"-----| Practice {PRACTICE}, Exercise {EXCERCISE} |------")
sequence_list = ([Seq(), Seq("ACTGA"), Seq("Invalid sequence")])
for i, sequence in enumerate(sequence_list):
    print(f"Sequence {i + 1}: (Length: {sequence.len()}) {sequence}")
    print(f"\tBases: {sequence.count()}")
    print(f"\tRev:  {sequence.reverse()}")
    print(f"\tComp: {sequence.complement()}")

