import socket

# SERVER IP, PORT
# Write here the correct parameter for connecting to the
# Teacher's server
SERVER_PORT = 8081
SERVER_IP = ""  # it depends on the machine the server is running

# First, create the socket
# We will always use these parameters: AF_INET y SOCK_STREAM
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# establish the connection to the Server (IP, PORT)
s.connect((SERVER_IP, SERVER_PORT))  # relation direct con el accept

# Send data. No strings can be sent, only bytes
# It necessary to encode the string into bytes
s.send(str.encode("HELLO FROM THE CLIENT!!!"))  # relation direct con el rcv
# un metodo estatico de la clase string que convierte los strings in bytes(011001..): encode

# Close the socket
s.close()  # socket of the client
