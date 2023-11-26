import socket
import json
import myFunction

class POP3CLIENT:
    
    mailNum : 0
    def __init__(self,server,port,addr,userEmail,password,clientSocket):
        self.server = server
        self.port = port
        self.addr = addr
        self.userEmail = userEmail
        self.password = password
        self.clientSocket = clientSocket
    
    def connect_server(self):
        
        print("Establist contact to pop3 server {} at port {}".format(self.server,self.port))
        self.clientSocket.connect(self.addr)
        #check connect fail
        recv = self.clientSocket.recv(1024).decode()
        print(recv)
        if recv[0:3].lower() == '-err':
            raise Exception('Negative response from server. Stop program')


    def send_user_cmd(self):
        userCmd = "USER {}\r\n".format(self.userEmail)
        self.clientSocket.send(userCmd.encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)
        if recv[0:3].lower() == '-err':
            raise Exception('Negative response from server. Stop program')

    
    def send_pass_cmd(self):
        passCmd = "PASS {}\r\n".format(self.password)
        self.clientSocket.send(passCmd.encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)
        if recv[0:3].lower() == '-err':
            raise Exception('Negative response from server. Stop program')

    def send_stat_cmd(self):
        statCmd = "STAT\r\n"
        self.clientSocket.send(statCmd.encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)
        if recv[0:3].lower() == '-err':
            raise Exception ('Negative response from server. Stop program')

    def send_list_cmd(self):
        listCmd = "LIST\r\n"
        self.clientSocket.send(listCmd.encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)
        if recv[0:3].lower() == '-err':
            raise Exception('Negative response from server. Stop program')


    def send_retr_cmd(self):
        for i in range (1,2):
            retrCmd = "RETR {}\r\n".format(input("Enter mail your want to read : "))
            self.clientSocket.send(retrCmd.encode())
            recv = self.clientSocket.recv(1024).decode()
            print (recv)
            if recv[0:4].lower() == '-err':
                raise Exception('Negative response from server. Stop program')
            
            if(myFunction.saveMail(recv,self.userEmail)):
                print("Save mail successfully")
            else : 
                print("Can't save mail")

    def send_quit_cmd(self):
        # QUIT
        quitCmd = "QUIT\r\n"
        self.clientSocket.send(quitCmd.encode())
        print("Close connection")

#========================================================================
pop3Port = 3335
pop3Sever = "127.0.0.1"
pop3Addr = (pop3Sever,pop3Port)
userEmail = "mail1@gmail.com"
userPass = "123"
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client = POP3CLIENT(pop3Sever,pop3Port,pop3Addr,userEmail,userPass,clientSocket)
    #Connect server
    client.connect_server()
    # USER
    client.send_user_cmd()
    # PASS
    client.send_pass_cmd()
    # STAT
    client.send_stat_cmd()
    # LIST
    client.send_list_cmd()
    # RETR
    client.send_retr_cmd()

except Exception as e:
    print("Error occurred: ",e)
finally:
    # QUIT
    client.send_quit_cmd()
