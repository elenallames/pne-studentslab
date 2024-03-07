import socket
import termcolor
from seq import Seq

seq_list = ["ACTGGGTACCATGACTAAGTCCAATGCATGCA", "ACGTGG", "AAGTGG", "AAATGG", "AAAAGG"]
FILENAMES = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]


class Server:
    def __init__(self):

        # Configure the Server's IP and PORT
        PORT = 8080
        IP = "127.0.0.1"  # it depends on the machine the server is running

        # create an INET, STREAMing socket
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            serversocket.bind((IP, PORT))
            # become a server socket
            serversocket.listen()
            print("SEQ Server is configured!")

            while True:
                # accept connections from outside
                print(f"Waiting for clients...")
                (clientsocket, address) = serversocket.accept()

                # Read the message from the client, if any
                msg = clientsocket.recv(2048).decode("utf-8")
                response = self.calculate_response(str(msg))

                # Send the message
                message = "Hello from the teacher's server\n"
                send_bytes = str.encode(response)
                # We must write bytes, not a string
                clientsocket.send(send_bytes)
                clientsocket.close()

        except socket.error:
            print(f"Problems using ip {IP} port {PORT}. Is the IP correct? Do you have port permission?")

        except KeyboardInterrupt:
            print("Server stopped by the user")
            serversocket.close()

    def calculate_response(self, msg):
        if msg.startswith("PING"):
            termcolor.cprint("PING command!", "green")
            return "OK!\n"


c = Server()
