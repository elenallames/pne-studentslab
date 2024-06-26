# Exercise 5
from Client0 import Client
from seq import Seq
import os

PRACTICE = 2
EXERCISE = 5
GENE = "FRAT1"
NUMBER_OF_FRAGMENTS = 5
NUMBER_OF_BASES = 10

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

IP = "192.168.0.30"
PORT = 8081

client_object = Client(IP, PORT)
print(client_object)

filename_gene = os.path.join("..", "sequences", GENE + ".txt")
try:
    sequence = Seq()
    sequence.read_fasta(filename_gene)
    print(f"Gene {GENE}: {sequence}")

    start = 0
    end = NUMBER_OF_BASES
    for i in range(1, NUMBER_OF_FRAGMENTS + 1):
        sequence_str = str(sequence)
        fragment = sequence_str[start:end]
        msg = f"Fragment {i}: {fragment}"
        print(msg)
        client_object.talk(msg)

        start += NUMBER_OF_BASES
        end += NUMBER_OF_BASES
except FileNotFoundError:
    print(f"[ERROR]: file '{filename_gene}' not found")