#Exercise5
from Seq0 import *
genes = ["U5", "ADA", "FRAT1", "FXN"]
print("-----| Exercise 5 |------")
for gene in genes:
    print("Gene", gene, ":", seq_count(gene))