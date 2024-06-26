from pathlib import Path

def seq_ping():
    print("OK")

def seq_read_fasta(filename):
    folder = "../sequences/"
    filepath = Path(folder) / (filename + ".txt")
    file_contents = filepath.read_text()
    header_end = file_contents.find("\n")
    body = file_contents[header_end + 1:].replace("\n", "")
    return body

def seq_len(seq):
    gene_sequence = seq_read_fasta(seq)
    print(f"Gene {seq} -> Length: {len(gene_sequence)}")

def seq_count_base(seq, bases):
    gene = seq_read_fasta(seq)
    counts = {base: gene.count(base) for base in bases}
    print(f"Gene {seq}:")
    for base, count in counts.items():
        print(f"   {base}: {count}")

def seq_count(seq):
    gene = seq_read_fasta(seq)
    bases = ['A', 'T', 'C', 'G']
    counts = {base: gene.count(base) for base in bases}
    print(f"Gene {seq}: {counts}")

def seq_reverse(seq):
    n = 20
    gene = seq_read_fasta(seq)
    fragment = gene[:n]
    reverse_fragment = fragment[::-1]
    print(f"Gene {seq}\nFragment: {fragment}\nReverse: {reverse_fragment}")

def seq_complement(seq):
    gene = seq_read_fasta(seq)
    fragment = gene[:20]
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    complement_fragment = ''.join(complement[base] for base in fragment)
    print(f"Gene {seq}\nFrag: {fragment}\nComp: {complement_fragment}")

def processing_the_genes(seq):
    gene = seq_read_fasta(seq)
    bases = ['A', 'T', 'C', 'G']
    counts = {base: gene.count(base) for base in bases}
    most_frequent_base = max(counts, key=counts.get)
    print(f"Gene {seq}: Most frequent base: {most_frequent_base}")
