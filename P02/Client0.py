class Client:
    def __init__(self, ip, port):  # constructor de los objets de la clase
        self.ip = ip
        self.port = port

    def __str__(self):
        return f"Connection to SERVER at {self.ip}, PORT: {self.port}"

    def ping(self):
        print("OK!")
    # c = Client(ip, port)
    # c.ping()

    def talk(self, msg):
        import socket
        # -- Create the socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # establish the connection to the Server (IP, PORT)
        client_socket.connect((self.ip, self.port))  # tuple

        # Send data.
        msg_bytes = str.encode(msg)
        client_socket.send(msg_bytes)   # client_socket.send(str.encode(msg))

        # Receive data
        response_bytes = client_socket.recv(2048)
        response = response_bytes.decode("utf-8")
        # response = client_socket.recv(2048).decode("utf-8")

        # Close the socket
        client_socket.close()

        # Return the response
        return response
