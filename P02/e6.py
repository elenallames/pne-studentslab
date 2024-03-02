from Client0 import Client
from Seq1 import *
import os
PRACTICE = 2
EXERCISE = 6
print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")
IP = "212.128.255.64"
PORT = 8081
c1 = Client(IP, PORT)
print(c1)
PORT = 8081
IP = "172.17.0.1"
c2 = Client(IP, PORT)
print(c2)
s = Seq()
s.read_fasta("FRAT1")
msg =(f"Sending FRAT1 Gene to the server, in fragments of 10 bases...")
first_message_to_first_server = c1.talk(msg)
first_message_to_second_server = c2.talk(msg)
msg2 = str(s)
second_message_to_first_server = c1.talk(f"Gene FRAT1: {msg2}")
second_message_to_second_server = c2.talk(f"Gene FRAT1: {msg2}")
print(f"Gene FRAT1: {msg2}")
for f in range(1, 11):
    index = (f-1) * 10
    fragment = msg2[index: index + 10]
    print(f"Fragment {f}: {fragment}")
    if f % 2 == 0:
        message = c2.talk(f"Fragment {f}: {fragment}")
    else:
        message = c1.talk(f"Fragment {f}: {fragment}")