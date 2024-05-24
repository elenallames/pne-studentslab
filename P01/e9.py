# Exercise 9
import os
from seq import Seq

PRACTICE = 1
EXCERCISE = 9

print(f"-----| Practice {PRACTICE}, Exercise {EXCERCISE} |------")

# -- Create a Null sequence
s = Seq()

GENE = "U5"

filename = os.path.join("..", "sequences", GENE + ".txt")
try:
    s.read_fasta(filename)
    print(f"Sequence: (Length: {s.len()}) {s}")
    print(f"\tBases: {s.count()}")
    print(f"\tRev:  {s.reverse()}")
    print(f"\tComp: {s.complement()}")
except FileNotFoundError:
    print(f"[ERROR]: file ´{filename}´ not found")
