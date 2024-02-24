from Seq1 import *
print("-----| Practice 1, Exercise 6 |------")
s1 = Seq()
s2 = Seq("ACTGA")
s3 = Seq("Invalid sequence")

print(f"Sequence", 1, ": (Length:", seq_len(s1), ")", s1)
count_seq(s1)
print(f"Sequence", 2, ": (Length:", seq_len(s2), ")", s2)
count_seq(s2)
print(f"Sequence", 3, ": (Length:", seq_len(s3), ")", s3)
count_seq(s3)