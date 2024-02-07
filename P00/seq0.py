from pathlib import Path
def seq_ping():
    print("OK")

def seq_read_fasta(filename):
    file_contents = Path(filename).read_text()

    header = file_contents.find("\n")

    body = file_contents[header:]

    list_contents = body.replace("\n", "")

    print("The first 20 bases are:")
    print(list_contents[:20])

def seq_len(seq):
    FOLDER = "../sequences/"
    FILENAME = seq + ".fa"
    file_contents = Path(FOLDER + FILENAME).read_text()
    header = file_contents.find("\n")

    body = file_contents[header:]

    list_contents = body.replace("\n", "")
    print("Gene", seq + "-> Length:", len(list_contents))

def seq_count_base(seq,base):
    genes = []






