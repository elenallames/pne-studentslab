import socket
import termcolor
from seq import Seq
import os

IP = "127.0.0.1"
PORT = 8080
SEQUENCES = ["ADA", "FRAT1", "FXN", "RNU6_269P", "U5"]

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    server_socket.bind((IP, PORT))
    server_socket.listen()

    print("SEQ Server configured!")

    while True:
        print(f"Waiting for connections at ({IP}:{PORT})...")
        (client_socket, client_address) = server_socket.accept()

        request_bytes = client_socket.recv(2048)
        request = request_bytes.decode()

        lines = request.splitlines()
        slices = lines[0].split(' ')
        print(f"Slices: {slices}")
        command = slices[0]
        print(f"Command: {command}")
        if command == "PING":
            response = "OK!\n"
        elif command == "GET":
            n = int(slices[1])
            gene = SEQUENCES[n]
            s = Seq()
            filename = os.path.join("..", "sequences", gene + ".txt")
            s.read_fasta(filename)
            response = str(s)

        print(response)
        response_bytes = response.encode()
        client_socket.send(response_bytes)

        client_socket.close()
except socket.error:
    print(f"Problems using port {PORT}. Do you have permission?")
except KeyboardInterrupt:
    print("Server stopped by the admin")
    server_socket.close()

