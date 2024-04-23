# Exercise 10
import os
from seq import Seq

PRACTICE = 1
EXCERCISE = 10

print(f"-----| Practice {PRACTICE}, Exercise {EXCERCISE} |------")
genes = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]

for g in genes:
    filename = os.path.join("..", "genes", g + ".txt")
    try:
        s = Seq()
        s.read_fasta(filename)
        print(f"Gene {g}: Most frequent Base: {s.max_base()}")
    except FileNotFoundError:
        print(f"[ERROR]: file ´{filename}´ not found")
