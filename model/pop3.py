import socket
from model import myFunction

pop3Port = 3335
pop3Sever = "127.0.0.1"
pop3Addr = (pop3Sever, pop3Port)

# userEmail = "codingAkerman@fit.hcmus.edu.vn"
userEmail = "mail1@gmail.com"
userPass = "123"

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Establist contact to pop3 server {} at port {}".format(pop3Sever, pop3Port))
clientSocket.connect(pop3Addr)

# check connect fail
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[0:3].lower() == '-err':
    print('Negative response from server. Stop program')

# USER
# userEmail = input("Enter your email: ")
userCmd = "USER {}\r\n".format(userEmail)
clientSocket.send(userCmd.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[0:3].lower() == '-err':
    print('Negative response from server. Stop program')

# PASS
passCmd = "PASS {}\r\n".format(userPass)
clientSocket.send(passCmd.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[0:3].lower() == '-err':
    print('Negative response from server. Stop program')

try:
    # STAT
    statCmd = "STAT\r\n"
    clientSocket.send(statCmd.encode())
    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[0:3].lower() == '-err':
        raise Exception('Negative response from server. Stop program')

    # LIST
    listCmd = "LIST\r\n"
    clientSocket.send(listCmd.encode())
    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[0:3].lower() == '-err':
        raise Exception('Negative response from server. Stop program')

    # RETR
    for i in range(1, 2):
        retrCmd = "RETR {}\r\n".format(input("Enter mail you want to read : "))
        clientSocket.send(retrCmd.encode())
        recv = clientSocket.recv(1024).decode()
        print("-------------------------Data = ", recv)
        if recv[0:4].lower() == '-err':
            raise Exception('Negative response from server. Stop program')

        if (myFunction.saveMail(recv, userEmail)):
            print("Save mail successfully")
        else:
            print("Can't save mail")

except Exception as e:
    print("Error occurred: ", e)

finally:
    # QUIT
    quitCmd = "QUIT\r\n"
    clientSocket.send(quitCmd.encode())
    recv = clientSocket.recv(1024)
