# Exercise 1
from Client0 import Client

PRACTICE = 2
EXERCISE = 1

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

# -- Parameters of the server to talk to
IP = "212.128.255.17"  # the server IP address
PORT = 8081

# -- Create a client object
client_object = Client(IP, PORT)

# -- Test the ping method
client_object.ping()
