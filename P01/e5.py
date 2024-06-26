# Exercise 5
from seq import Seq

PRACTICE = 1
EXCERCISE = 5

print(f"-----| Practice {PRACTICE}, Exercise {EXCERCISE} |------")
sequence_list = [Seq(), Seq("ACTGA"), Seq("Invalid sequence")]
for i, sequence in enumerate(sequence_list):
    print(f"Sequence {i + 1}: (Length: {sequence.len()}) {sequence}")
    for b in ['A', 'T', 'C', 'G']:
        print(f"\t{b}: {sequence.count_base(b)}", end="")
    print()
