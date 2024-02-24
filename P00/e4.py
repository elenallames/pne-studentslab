#Exercise4
from Seq0 import *
print("-----| Exercise 4 |------")
genes = ["ADA", "U5", "FRAT1", "FXN"]
bases = ["A", "C", "T", "G"]
for gene in genes:
    print("Gene", gene, ":")
    for base in bases:
        seq_count_base(gene, base)
    print()