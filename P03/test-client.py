from client import Client

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8080
PRACTICE = 3
EXERCISE = 7
N = 5
BASES = "ACCTCCTCTCCAGCAATGCCAACCCCAGTCCAGGCCCCCATCCGCCCAGGATCTCGATCA"
GENES = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]


def main():
    print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

    # Initialize the client
    client = Client(SERVER_IP, SERVER_PORT)
    print(client)

    # Test PING command
    print("* Testing PING...")
    response = client.talk("PING")
    print(response)

    # Test GET command for a range of indices
    print("* Testing GET...")
    for n in range(N):
        response = client.talk(f"GET {n}")
        print(f"GET {n}: {response}")

    print()

    # Test INFO command with the provided BASES sequence
    print("* Testing INFO...")
    response = client.talk(f"INFO {BASES}")
    print(response)

    # Test COMP command with the provided BASES sequence
    print("* Testing COMP...")
    print(f"COMP {BASES}")
    response = client.talk(f"COMP {BASES}")
    print(response)

    # Test REV command with the provided BASES sequence
    print("* Testing REV...")
    print(f"REV {BASES}")
    response = client.talk(f"REV {BASES}")
    print(response)

    print()

    # Test GENE command with each gene in the GENES list
    print("* Testing GENE...")
    for gene in GENES:
        print(f"GENE {gene}")
        response = client.talk(f"GENE {gene}")
        print(response)
        print()


if __name__ == "__main__":
    main()
