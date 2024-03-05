import socket
import termcolor
# Configure the Server's IP and PORT
PORT = 8081
IP = "212.128.255.88" # this IP address is local, so only requests from the same machine are possible

MAX_OPEN_REQUESTS = 5

# Counting the number of connections
number_con = 0
# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    serversocket.bind((IP, PORT))
    # become a server socket
    # MAX_OPEN_REQUESTS connect requests before refusing outside connections
    serversocket.listen(
        MAX_OPEN_REQUESTS)  # have que a partir de esta instruccion se puedan conectar clientes(canal de comunicacion bidireccional)
    # determina cuantos clientes  a la vez pueden conectarse al servidor

    while True:
        # accept connections from outside
        print(f"Waiting for connections at {IP}, {PORT}")
        (clientsocket, address) = serversocket.accept()  # mi codigo se detien ahi hasta que no se conecte un cliente
        # address(IP_client <str>, PORT_client <int>)
        # Another connection!e
        number_con += 1  # se acaba de conectar un cliente

        # Print the connection number
        print(f"CONNECTION: {number_con}. From the IP: {address}")
except socket.error:
    print(f"Problems using ip {IP} port {PORT}. Is the IP correct? Do you have port permission?")

except KeyboardInterrupt:
    print("Server stopped by the user")
    serversocket.close()

# -- Step 1: create the socket
ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# -- Step 2: Bind the socket to server's IP and PORT
ls.bind((IP, PORT))

# -- Step 3: Configure the socket for listening, server ready to listen different request
ls.listen()

print("The server is configured!")

while True:
    (rs, address) = ls.accept()
    print("Waiting for Clients to connect echo")
    print(f"A client has connected to the server!")
    print("Client IP,PORT: ", )
    msg = rs.recv(2048).decode("utf-8")
    print("Message received: " + termcolor.colored(msg, "green"))
    newMsg = "ECHO:  " + msg
    rs.send(newMsg.encode())
    rs.close()
# -- Close the socket
ls.close()
