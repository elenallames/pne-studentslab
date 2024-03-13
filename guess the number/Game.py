import socket
import random

class NumberGuesser:
    def __init__(self):
        secret_number = random.randint(1, 100)
        print("The secret number is:", secret_number)
        self.secret_number = secret_number
        self.attempts = []

    def guess(self, msg):
        msg = int(msg)
        if msg == self.secret_number:
            hint = "You guessed the secret number after x tries:)"
        elif msg < self.secret_number:
            hint = "The secret number is higher"
        elif msg > self.secret_number:
            hint = "The secret number is lower"
        self.attempts.append(msg)
        return hint


PORT = 8081
IP = "212.128.255.88"  # it depends on the machine the server is running
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    serversocket.bind((IP, PORT))
    serversocket.listen()
    ng = NumberGuesser()
    flag = True
    while flag:
        print(f"Waiting for clients at {IP}, {PORT}")
        (clientsocket, address) = serversocket.accept()

        print(f"Client connected, number is being generated!")

        print(f"Random number generated, please, enter your try")
        # Read the message from the client, if any
        msg = clientsocket.recv(2048).decode("utf-8")
        print("Message from client: {}".format(msg))
        rsp = ng.guess(msg)
        # Send the message
        send_bytes = str.encode(rsp)
        # We must write bytes, not a string
        clientsocket.send(send_bytes)
        clientsocket.close()

except socket.error:
    print("Problems using ip {} port {}. Is the IP correct? Do you have port permission?".format(IP, PORT))

except KeyboardInterrupt:
    print("Server stopped by the user")
    serversocket.close()
