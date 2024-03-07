import socket
import termcolor

PORT = 8081
IP = "127.0.0.1"  # this IP address is local, so only requests from the same machine are possible

# -- Step 1: create the socket
ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# -- Step 2: Bind the socket to server's IP and PORT
ls.bind((IP, PORT))

# -- Step 3: Configure the socket for listening, server ready to listen different request
ls.listen()

i = 0

number_con = 0
clients_list = []
flag = True
while flag:
    number_con += 1
    (rs, address) = ls.accept()
    Msg = f"CONNECTION {i}. Client IP,PORT: {address}"
    rs.send(Msg.encode())
    print("To server:" + termcolor.colored(f"Message{i}", "blue"))
    msg = rs.recv(2048).decode("utf-8")
    print("From server: " + termcolor.colored(msg, "green"))
    newMsg = "\nECHO:  " + msg
    rs.send(newMsg.encode())
    rs.close()
    if number_con == 5:
        flag = False
    i += 1
    clients_list.append(address)

message = "The following clients has connected to server"
rs.send(message.encode())
for i in range(len(clients_list)):
    message = f"Client {i}: {clients_list[i]}"
    rs.send(message.encode())
# -- Close the socket
ls.close()
