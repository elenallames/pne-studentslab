# Exercise 4
from Client0 import Client
from seq import Seq
import os

PRACTICE = 2
EXERCISE = 4
FILENAMES = ["U5", "FRAT1", "ADA"]

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

IP = "192.168.0.33"
PORT = 8081

client_object = Client(IP, PORT)
print(client_object)

for g in FILENAMES:
    filename_genes = os.path.join("..", "sequences", g + ".txt")
    try:
        s = Seq()  # s.__str__()
        s.read_fasta(filename_genes)

        msg = f"Sending {g} Gene to the server..."
        print(f"To Server: {msg}")
        response = client_object.talk(msg)
        print(f"From Server: {response}")

        msg = str(s)    # msg = f"{s}" / s.__str__()
        print(f"To Server: {msg}")
        response = client_object.talk(msg)
        print(f"From Server: {response}")

    except FileNotFoundError:
        print(f"[ERROR]: file ´{filename_genes}´ not found")
