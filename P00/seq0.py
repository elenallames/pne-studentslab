from pathlib import Path
def seq_ping():
    print("OK")

def seq_read_fasta(filename):
    file_contents = Path(filename).read_text()
    index = file_contents.find("\n")
    list_contents = (file_contents[index:]).replace("\n", "")
    print("The first 20 bases are: ")
    print(list_contents[:20])

def seq_len(seq):
    FOLDER = "../sequences/"
    FILENAME = seq + ".txt"
    file_contents = Path(FOLDER + FILENAME).read_text()
    index = file_contents.find("\n")
    list_contents = (file_contents[index:]).replace("\n", "")
    print("Gene", seq + "-> Length: ", len(list_contents))

def seq_count_base(seq, base):
    genes = ["ADA", "U5", "FRAT1", "FXN"]
    bases = ["A", "T", "C", "G"]
    for i in genes:
        for b in bases:
            f = SEQUENCES + g + (".txt")
            bases = seq.read(f)
            total = seq.read(bases, b)








