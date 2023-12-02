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

        in_data = in_data.decode()
        cut_server_reply = in_data.find('Content-Type:')
        print ("cutserverreply: ",cut_server_reply)
        in_data = in_data[cut_server_reply:]
        print(f"================================================\n{in_data}")


        parsed_email = email.message_from_string(in_data)

        # Display email headers
        print(f"Date: { parsed_email['Date']}")
        print(f"From: {parsed_email['From']}", )
        print(f"To: {parsed_email['To']}" )
        print(f"Subject: {parsed_email['Subject']}")

        # Display email body
        # SAVE FILE
        for part in parsed_email.walk():
            if part.get_content_type() == 'text/plain':
                print(f"body content : {part.get_payload()}")
            #attach file
            elif part.get_content_type() == 'application/octet-stream':
                file_name = part.get_filename()
                file_type = file_name[file_name.find("."):]
                print(f"attachment name : {file_name}")
                save_file_path = os.path.join(os.path.dirname(__file__), '..','dest-attachment', '{}'.format(file_name))


                if file_type == ".pdf" or file_type == ".jpeg" or file_type == ".png" or file_type == ".docx" or file_type == ".zip" :
                    file_content = part.get_payload(decode=True)
                    with open(save_file_path, 'wb') as f:
                        f.write(file_content)
                    print(f"--------------PDF file {file_name} saved.------------")
                if file_type == ".txt":
                    file_content = part.get_payload(decode=False)
                    file_content = file_content.encode()
                    file_content = base64.b64decode(file_content)
                    file_content = file_content.decode()
                    with open(save_file_path, 'w') as f:
                        f.write(file_content)



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

