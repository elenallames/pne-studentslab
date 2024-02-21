#Exercise3
import os
from Seq0 import *

GENES = ["U5", "ADA.txt", "FRAT1", "FXN"]

for gene in GENES:
    filename = os.path.join("..", "sequences", gene + ".txt")
    try:
        dna_sequence = seq_read_fasta(filename)
        print(f"Gene {gene} -> Length: {seq_len(dna_sequence)}")
    except FileNotFoundError:
        print(f"[ERROR]: file '{filename}' not found")


