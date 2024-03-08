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

c = Client(IP, PORT)
print(c)

filename = os.path.join("..", "sequences", GENE + ".txt")
try:
    s = Seq()
    s.read_fasta(filename)
    print(f"Gene {GENE}: {s}")

    start = 0
    end = NUMBER_OF_BASES
    for i in range(1, NUMBER_OF_FRAGMENTS + 1):
        s_str = str(s)
        fragment = s_str[start:end]
        msg = f"Fragment {i}: {fragment}"
        print(msg)
        c.talk(msg)

        start += NUMBER_OF_BASES
        end += NUMBER_OF_BASES
except FileNotFoundError:
    print(f"[ERROR]: file '{filename}' not found")