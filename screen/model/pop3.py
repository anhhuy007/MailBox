import socket
import json
import myFunction
import email
import base64
import os
import random

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
        retrCmd = "RETR {}\r\n".format(input("Enter mail your want to read : "))
        self.clientSocket.send(retrCmd.encode())


        in_data = b''
        self.clientSocket.settimeout(1)  
        while True:
            try:
                recv = self.clientSocket.recv(4096)
                if recv[0:4].lower() == '-err':
                    raise Exception('Negative response from server. Stop program')
                if not recv:
                    break
                in_data += recv
            except socket.timeout:
                break

        # cut server reply
        in_data = in_data.decode()
        cut_server_reply = in_data.find('Content-Type:')
        in_data = in_data[cut_server_reply:]
        print(f"================================================\n{in_data}")

        parsed_email = email.message_from_string(in_data)
        dateInfo = parsed_email['Date']
        
        # save mail
        if(myFunction.save_mail(parsed_email, self.userEmail)):
            print("Save mail success")
        else:
            print("Save mail fail")

        if(input("Do you want to save attach file in this mail ? (y/n) : ").lower() == "y"):
            if(myFunction.save_attach("mailBox\\"+ myFunction.getFileName(dateInfo) + ".json")):
                print("Save attach success")
            else:
                print("Save attach fail")


    def send_quit_cmd(self):
        # QUIT
        quitCmd = "QUIT\r\n"
        self.clientSocket.send(quitCmd.encode())
        print("Close connection")

#========================================================================
pop3Port = 3335
pop3Sever = "127.0.0.1"
pop3Addr = (pop3Sever,pop3Port)
userEmail = "codingAkerman@fit.hcmus.edu.vn"
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
    # QUIT
    client.send_quit_cmd()
except Exception as e:
    print("Error occurred: ",e)
finally:
    clientSocket.close()
    print ("close server")

