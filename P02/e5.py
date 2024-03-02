from Client0 import Client
from Seq1 import *
import os
PRACTICE = 2
EXERCISE = 5

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")
IP = "212.128.255.64"
PORT = 8081
c = Client(IP, PORT)
print(c)
s = Seq()
s.read_fasta("FRAT1")
msg =(f"Sending FRAT1 Gene to the server, in fragments of 10 bases...")
first_message = c.talk(msg)
msg2 = str(s)
second_message = c.talk(f"Gene FRAT1: {msg2}")
print(f"Gene FRAT1: {msg2}")
for f in range(1, 6):
    index = (f-1) * 10
    fragment = msg2[index: index + 10]
    message = c.talk(f"Fragment {f}: {fragment}")
    print(f"Fragment {f}: {fragment}")