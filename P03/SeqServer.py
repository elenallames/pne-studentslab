import socket
from seq import Seq
import os

IP = "127.0.0.1"
PORT = 8080
SEQUENCES = ["AAACCGTA", "GATA", "AACGT", "CCTGC", "ACGTACGT"]


def handle_client(client_socket):
    try:
        request_bytes = client_socket.recv(2048)
        request = request_bytes.decode()
        lines = request.splitlines()
        slices = lines[0].split(' ')
        command = slices[0].upper()

        print(f"Slices: {slices}")
        print(f"Command: {command}")

        if command == "PING":
            response = "OK!\n"
        elif command == "GET":
            n = int(slices[1])
            bases = SEQUENCES[n]
            s = Seq(bases)
            response = str(s) + "\n"
        elif command == "INFO":
            bases = slices[1]
            s = Seq(bases)
            response = s.info() + "\n"
        elif command == "COMP":
            bases = slices[1]
            s = Seq(bases)
            response = s.complement() + "\n"
        elif command == "REV":
            bases = slices[1]
            s = Seq(bases)
            response = s.reverse() + "\n"
        elif command == "GENE":
            gene = slices[1]
            s = Seq()
            filename = os.path.join("..", "sequences", f"{gene}.txt")
            s.read_fasta(filename)
            response = str(s) + "\n"
        else:
            response = "ERROR: Unknown command\n"

        print(response)
        client_socket.sendall(response.encode())
    except Exception as e:
        print(f"Error handling client request: {e}")
        client_socket.sendall(b"ERROR: An error occurred\n")
    finally:
        client_socket.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server_socket.bind((IP, PORT))
        server_socket.listen()
        print("SEQ Server configured!")

        while True:
            print(f"Waiting for connections at ({IP}:{PORT})...")
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")
            handle_client(client_socket)
    except socket.error as e:
        print(f"Socket error: {e}")
    except KeyboardInterrupt:
        print("Server stopped by the admin")
    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()
