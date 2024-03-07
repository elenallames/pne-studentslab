i = 0
count = 0

flag = True
while flag:
    dna_sequence = input("Enter a sequence: ").upper()
    total_letters = 0
    for c in dna_sequence:
        if c == "A" or c == "G" or c == "C" or c == "T":
            total_letters += 1
    if total_letters == len(dna_sequence):
        flag = False
    else:
        print("The dna sequence is incorrect")

dna_sequence = input("Enter a sequence: ").upper()
dna_sequence_length = len(dna_sequence)
print(f"Total length: {dna_sequence_length}")
c_a = 0
c_c = 0
c_g = 0
c_t = 0
for c in dna_sequence:
    if c == "A":
        c_a += 1
    elif c == "G":
        c_g += 1
    elif c == "T":
        c_t += 1
    elif c == "C":
        c_c += 1
print("Total number of appearances: ", "\nA:", c_a, "\nC:", c_c, "\nG:", c_g, "\nT:", c_t)
