from client import Client

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8080
PRACTICE = 3
EXCERCISE = 7
N = 5
BASES = "ACCTCCTCTCCAGCAATGCCAACCCCAGTCCAGGCCCCCATCCGCCCAGGATCTCGATCA"
GENES = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]

print(f"-----| Practice {PRACTICE}, Exercise {EXCERCISE} |------")

c = Client(SERVER_IP, SERVER_PORT)
print(c)

print("* Testing PING...")
response = c.talk("PING")
print(response)

print("* Testing GET...")
for n in range(N):
    response = c.talk(f"GET {n}")
    print(f"GET {n}: {response}")

print()

print("* Testing INFO...")
response = c.talk(f"INFO {BASES}")
print(response)

print("* Testing COMP...")
print(f"COMP {BASES}")
response = c.talk(f"COMP {BASES}")
print(response)

print("* Testing REV...")
print(f"REV {BASES}")
response = c.talk(f"REV {BASES}")
print(response)

print()

print("* Testing GENE...")
for gene in GENES:
    print(f"GENE {gene}")
    response = c.talk(f"GENE {gene}")
    print(response)
    print()
