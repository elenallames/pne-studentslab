# Exercise 2
from seq import Seq

PRACTICE = 1
EXCERCISE = 2

print(f"-----| Practice {PRACTICE}, Exercise {EXCERCISE} |------")

sequence_list = [Seq(), Seq("TATAC")]
for i, sequence in enumerate(sequence_list):
    print(f"Sequence {i + 1}: {sequence}")





