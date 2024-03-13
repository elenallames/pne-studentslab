from Client0 import *
PORT = 8080
IP = "127.0.0.1"
c = Client(IP, PORT)
print(c)
while True:
    number = input("Enter a number between 1 and 100")
    guess = c.talk(number)
    print(guess)