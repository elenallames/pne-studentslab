# Exercise 4
from seq import Seq

PRACTICE = 1
EXCERCISE = 4

print(f"-----| Practice {PRACTICE}, Exercise {EXCERCISE} |------")
sequence_list = [Seq(), Seq("ACTGA"), Seq("Invalid sequence")]
for i, sequence in enumerate(sequence_list):
    print(f"Sequence {i + 1}: (Length: {sequence.len()}) {sequence}")
