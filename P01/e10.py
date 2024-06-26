# Exercise 10
import os
from seq import Seq

PRACTICE = 1
EXCERCISE = 10

print(f"-----| Practice {PRACTICE}, Exercise {EXCERCISE} |------")
filenames = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]

for f in filenames:
    filenames_genes = os.path.join("..", "sequences", f + ".txt")
    try:
        sequence = Seq()
        sequence.read_fasta(filenames_genes)
        print(f"Gene {f}: Most frequent Base: {sequence.max_base()}")
    except FileNotFoundError:
        print(f"[ERROR]: file ´{filenames_genes}´ not found")
