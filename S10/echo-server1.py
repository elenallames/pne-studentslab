import socket
import termcolor

# Configure the Server's IP and PORT
PORT = 8081
IP = "212.128.255.17" # this IP address is local, so only requests from the same machine are possible

# -- Step 1: create the socket
ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# -- Step 2: Bind the socket to server's IP and PORT
ls.bind((IP, PORT))

# -- Step 3: Configure the socket for listening, server ready to listen different request
ls.listen()

print("The server is configured!")

while True:
    (rs, address) = ls.accept()
    print("Waiting for Clients to connectecho")
    print(f"A client has connected to the server!")
    msg = rs.recv(2048).decode("utf-8")
    print("Message received: " + termcolor.colored(msg, "yellow"))
    newMsg = "ECHO:  " + msg
    rs.send(newMsg.encode())
    rs.close()
# -- Close the socket
ls.close()



