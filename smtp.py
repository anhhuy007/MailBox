import socket
import datetime
import myFunction



class SMTPCLIENT:
    
    recipientList = []
    sendMethod = 0
    def __init__(self, server, port, addr, clientAddr, userEmail, clientSocket ):
        self.server = server
        self.port = port
        self.addr = addr
        self.userEmail = userEmail      #mail from login
        self.clientSocket = clientSocket
        self.clientAddr = clientAddr

    def connect_server(self):
        print("Establist contact to mail server {} at port {}".format(self.server,self.port))
        self.clientSocket.connect(self.addr)

        #check connect fail
        recv = self.clientSocket.recv(1024).decode()
        print(recv)
        if recv[0:3] != '220':
             raise Exception('220 reply not received from server. Stop program')
    
    def send_helo_cmd(self):
            # Send HELO command and print server response.
        heloCmd = "HELO [{}]\r\n".format(self.clientAddr)
        self.clientSocket.send(heloCmd.encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)
        if recv[0:3] != '250':
            raise Exception('250 reply not received from server.')
    
    def send_mailfrom_cmd(self):
        # Send MAIL FROM command and print server response.
        mailFromCmd = "MAIL FROM: {}\r\n".format(self.userEmail)
        self.clientSocket.send(mailFromCmd.encode())
        recv =self.clientSocket.recv(1024).decode()
        print(recv)
        if recv[0:3] != '250':
            raise Exception('250 reply not received from server.')

    def send_rcpt_cmd(self):
        # Send RCPT TO command and print server response.
        recipentNum = 0
        self.sendMethod = input("Enter sendmethod [0:normal][1:CC][2:Bcc]: ")
        if self.sendMethod == "1" or self.sendMethod == "2":
            recipentNum = input("Enter number of recipents: ")
            for i in range(1,int(recipentNum)+1):
                recipient = input(f"Enter recipent {i}: ")
                self.recipientList.append(recipient)
                rcptToCmd = "RCPT TO: {}\r\n".format(recipient)
                self.clientSocket.send(rcptToCmd.encode())
                recv = self.clientSocket.recv(1024).decode()
                print(recv)
                if recv[0:3] != '250':
                    raise Exception('250 reply not received from server.')
        elif self.sendMethod == "0":
            recipient = input(f"Enter recipent: ")
            self.recipientList.append(recipient)
            rcptToCmd = "RCPT TO: {}\r\n".format(recipient)
            self.clientSocket.send(rcptToCmd.encode())
            recv = self.clientSocket.recv(1024).decode()
            print(recv)
            if recv[0:3] != '250':
                raise Exception('250 reply not received from server.')

        else:
            raise Exception('Invalid input. Stop program')
        
    def send_data_cmd(self):
        dataCmd = "DATA\r\n"
        self.clientSocket.send(dataCmd.encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)
        if recv[0:3] != '354':
            raise Exception('354 reply not received from server.')
        
        #header information: FROM, TO, DATE, SUBJECT
        
        fromInfo = "From: <{}>\r\n".format(self.userEmail)


        # toInfo= "To: <{}>\r\n".format(clientMail)
        toInfo  = myFunction.toInfoProccess(self.sendMethod,self.recipientList)

        dateInfo = "Date: " + myFunction.getTime() + "\r\n"
        subjectInfo = "Subject: {}\r\n".format(input("Enter Subject : "))
        headerInfo = fromInfo + toInfo + dateInfo + subjectInfo
        #  mail content
        mailContent = "Content: \r\n" +  input ("Enter mail content : ")


        # Message ends with a single period.
        dataSend =  headerInfo  +mailContent + "\r\n.\r\n"
        print("------------------------dataSend = ",dataSend)
        self.clientSocket.send(dataSend.encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)
        if recv[0:3] != '250':
            raise Exception('250 reply not received from server.')
        

    def send_quit_cmd(self):
        # Send QUIT command and get server response.
        dataCmd = "QUIT\r\n"
        self.clientSocket.send(dataCmd.encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)
        if recv[0:3] != '221':
            raise Exception('221 reply not received from server.')



#===========================================================================

mailserver = "127.0.0.1"
serverPort = 2225
serverAddr = (mailserver,serverPort)
clientAddr = "127.0.0.1"
clientMail = "codingAkerman@fit.hcmus.edu.vn"

# mailList
# mail1@gmail.com
# mail2@gmail.com
# mail3@gmail.com

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client = SMTPCLIENT(mailserver,serverPort,serverAddr,clientAddr,clientMail,clientSocket)

try:
    # Connect server
    client.connect_server()
    # Send HELO command and print server response.
    client.send_helo_cmd()
    # Send MAIL FROM command and print server response.
    client.send_mailfrom_cmd()
    # Send RCPT TO command and print server response.
    client.send_rcpt_cmd()
    # Send DATA command and print server response.
    client.send_data_cmd()
    


except Exception as e:
    print("Error occurred: ",e)

finally:
    client.send_quit_cmd()