import socket
import datetime
import myFunction
import myClass
import os
import base64
import traceback


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class SMTPCLIENT:
    
    to_recipient = []
    cc_list = []
    bcc_list = []
    ATTACHMENT_LIST = []

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
#--------------------------------------------------------------------------

        

    def send_rcpt_cmd(self):
    # Send RCPT TO command and print server response.
        recipientNum = 0
        #TO
        # self.to_recipient = input("Enter recipent: ")
        self.to_recipient = "codingAkerman@fit.hcmus.edu.vn"
        rcptToCmd = "RCPT TO: {}\r\n".format(self.to_recipient)
        self.clientSocket.send(rcptToCmd.encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)
        if recv[0:3] != '250':
            raise Exception('250 reply not received from server.')
        
        #CC LIST
        cc_recipient = input("Enter CC: (hit 0 to stop): ")
        while cc_recipient != "0":
            self.cc_list.append(cc_recipient)
            #send data
            rcptToCmd = "RCPT TO: {}\r\n".format(cc_recipient)
            self.clientSocket.send(rcptToCmd.encode())
            recv = self.clientSocket.recv(1024).decode()
            print(recv)
            if recv[0:3] != '250':
                raise Exception('250 reply not received from server.')
            cc_recipient = input("Enter CC (hit 0 to stop): ")

        #BCC LIST
        bcc_recipient = input("Enter Bcc (hit 0 to stop): ")
        # bcc_recipient = "0"
        while bcc_recipient != "0":
            self.bcc_list.append(bcc_recipient)
            #send data
            rcptToCmd = "RCPT TO: {}\r\n".format(bcc_recipient)
            self.clientSocket.send(rcptToCmd.encode())
            recv = self.clientSocket.recv(1024).decode()
            print(recv)
            if recv[0:3] != '250':
                raise Exception('250 reply not received from server.')
            bcc_recipient = input("Enter Bcc (hit 0 to stop): ")




#----------------------------------------------------------------
    def send_data_cmd(self):
        dataCmd = "DATA\r\n"
        self.clientSocket.send(dataCmd.encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)
        if recv[0:3] != '354':
            raise Exception('354 reply not received from server.')
        
        cc_list_str = ", ".join(self.cc_list)
        bcc_list_str = ", ".join(self.bcc_list)

        dateInfo = myFunction.getTime()
        #subjectInfo = input("Enter Subject : ")

        # mailContent =  input ("Enter mail content : ")

        # file_content_type = input("Enter file content type (text/plain | application/pdf): ")

        msg = MIMEMultipart()
        msg['Date'] = dateInfo
        msg['From'] = self.userEmail
        msg['To'] = self.to_recipient
        msg['Cc'] = cc_list_str
        msg['Bcc'] = bcc_list_str
        msg['Subject'] = "MIME test with 2 file time  "+ input ("MIME test Number: ")
        # Add body to email
        body = input("Enter mail content : ")
        msg.attach(MIMEText(body, 'plain'))

        # Attach file------------------------------------------------------
        file_name = input("Enter file name to attach (hit 0 to stop): ")
        while file_name != "0":
            file_path = os.path.join(os.path.dirname(__file__), '..','test-attachment', '{}'.format(file_name))
            attachment = open(file_path, 'rb')

            body_part = MIMEBase('application', 'octet-stream')
            body_part.set_payload(attachment.read())
            encoders.encode_base64(body_part)
            # part = base64.b64encode(part)
            body_part.add_header('Content-Disposition', f'attachment; filename= {file_name}')
            msg.attach(body_part)
            attachment.close()
            file_name = input("Enter file name to attach (hit 0 to stop): ")
            

        # send msg
        final_data = msg.as_string()
        self.clientSocket.send(final_data.encode() + '.\r\n'.encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)

        if recv[0:3] != '250':
            raise Exception('250 reply not received from server.')


    def send_quit_cmd(self):
        # Send QUIT command and get server response.
        quitCmd = "QUIT\r\n"
        self.clientSocket.send(quitCmd.encode())
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

    # Send QUIT command and print server response.
    client.send_quit_cmd()

except Exception as e:
    print("Error occurred: ",e)
    print(traceback.format_exc())

finally:
    clientSocket.close()
    print("Socket closed")