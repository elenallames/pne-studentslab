# Exercise 6
from Client0 import Client
from seq import Seq
import os


PRACTICE = 2
EXERCISE = 6
GENE = "FRAT1"
NUMBER_OF_FRAGMENTS = 10
NUMBER_OF_BASES = 10

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

IP = "192.168.0.30"
PORT1 = 8080
PORT2 = 8081

c1_object = Client(IP, PORT1)
print(c1_object)
c2_object = Client(IP, PORT2)
print(c2_object)

filename_gene = os.path.join("..", "sequences", GENE + ".txt")
try:
    sequence = Seq()
    sequence.read_fasta(filename_gene)
    print(f"Gene {GENE}: {sequence}")

    message = f"Sending {GENE} Gene to the server, in fragments of {NUMBER_OF_BASES} bases..."
    c1_object.talk(message)
    c2_object.talk(message)

    start = 0
    end = NUMBER_OF_BASES
    for i in range(1, NUMBER_OF_FRAGMENTS + 1):
        sequence_str = str(sequence)
        fragment = sequence_str[start:end]
        message = f"Fragment {i}: {fragment}"
        print(message)
        if i % 2 != 0:
            c1_object.talk(message)
        else:
            c2_object.talk(message)

        start += NUMBER_OF_BASES
        end += NUMBER_OF_BASES
except FileNotFoundError:
    print(f"[ERROR]: file '{filename_gene}' not found")
