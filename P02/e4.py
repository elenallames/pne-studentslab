# Exercise 4
from Client0 import Client
from seq import Seq
import os

PRACTICE = 2
EXERCISE = 4
GENES = ["U5", "FRAT1", "ADA"]

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

IP = "192.168.0.33"
PORT = 8081

c = Client(IP, PORT)
print(c)

for gene in GENES:
    filename = os.path.join("..", "genes", gene + ".txt")
    try:
        s = Seq()  # s.__str__()
        s.read_fasta(filename)

        msg = f"Sending {gene} Gene to the server..."
        print(f"To Server: {msg}")
        response = c.talk(msg)
        print(f"From Server: {response}")

        msg = str(s)    # msg = f"{s}" / s.__str__()
        print(f"To Server: {msg}")
        response = c.talk(msg)
        print(f"From Server: {response}")

    except FileNotFoundError:
        print(f"[ERROR]: file ´{filename}´ not found")
