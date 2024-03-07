dict_dna = {}
total = 0
with open("dna_count_file.txt", "r") as f:
    for line in f:
        for i in line:
            if i == 'A':
                if i not in dict_dna:
                    dict_dna['A'] = 1
                else:
                    dict_dna['A'] += 1
            elif i == 'C':
                if i not in dict_dna:
                    dict_dna['C'] = 1
                else:
                    dict_dna['C'] += 1
            elif i == 'T':
                if i not in dict_dna:
                    dict_dna['T'] = 1
                else:
                    dict_dna['T'] += 1
            elif i == 'G':
                if i not in dict_dna:
                    dict_dna['G'] = 1
                else:
                    dict_dna['G'] += 1
for key in dict_dna:
    total += dict_dna[key]  # total = dict_dna['A'] + dict_dna['C'] + dict_dna['T'] + dict_dna['G']
print("Introduce the sequence:", f, "\nTotal length:", total, "\n", dict_dna)



