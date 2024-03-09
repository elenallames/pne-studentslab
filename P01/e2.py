# Exercise 2
from seq import Seq

PRACTICE = 1
EXCERCISE = 2

print(f"-----| Practice {PRACTICE}, Exercise {EXCERCISE} |------")

seq_list = [Seq(), Seq("TATAC")]
for i, s in enumerate(seq_list):
    print(f"Sequence {i + 1}: {s}")





