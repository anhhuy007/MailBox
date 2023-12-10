import socket
import datetime
import os
import base64
import traceback

from model import myFunction

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class SMTPCLIENT:
    server = "127.0.0.1"
    port = 2225
    serverAddr = (server, port)
    clientAddr = "127.0.0.1"
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sendMethod = 0

    def __init__(self, userEmail, to_recipient, cc_list, bcc_list, subject, body, attachment_list):

        self.userEmail = userEmail  # mail from login
        self.to_recipient = to_recipient
        self.cc_list = cc_list
        self.bcc_list = bcc_list
        self.subject = subject
        self.body = body
        self.attachment_list = attachment_list

    def connect_server(self):
        print("Establist contact to mail server {} at port {}".format(self.server, self.port))
        self.clientSocket.connect(self.serverAddr)

        # check connect fail
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
        recv = self.clientSocket.recv(1024).decode()
        print(recv)
        if recv[0:3] != '250':
            raise Exception('250 reply not received from server.')

    # --------------------------------------------------------------------------

    def send_rcpt_cmd(self):
        # Send RCPT TO command and print server response.
        recipientNum = 0
        # TO
        rcptToCmd = "RCPT TO: {}\r\n".format(self.to_recipient)
        self.clientSocket.send(rcptToCmd.encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)
        if recv[0:3] != '250':
            raise Exception('250 reply not received from server.')

        # CC LIST + bcc list
        self.cc_list = self.cc_list.split(", ")
        self.bcc_list = self.bcc_list.split(", ")
        # CC LIST
        if self.cc_list != ['']:
            for cc_recipient in self.cc_list:
                rcptToCmd = "RCPT TO: {}\r\n".format(cc_recipient)
                self.clientSocket.send(rcptToCmd.encode())
                recv = self.clientSocket.recv(1024).decode()
                print(recv)
                if recv[0:3] != '250':
                    raise Exception('250 reply not received from server.')

        # BCC LIST
        if self.bcc_list != ['']:
            for bcc_recipient in self.bcc_list:
                # send data
                rcptToCmd = "RCPT TO: {}\r\n".format(bcc_recipient)
                self.clientSocket.send(rcptToCmd.encode())
                recv = self.clientSocket.recv(1024).decode()
                print(recv)
                if recv[0:3] != '250':
                    raise Exception('250 reply not received from server.')

    # ----------------------------------------------------------------
    def send_data_cmd(self):
        dataCmd = "DATA\r\n"
        self.clientSocket.send(dataCmd.encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)
        if recv[0:3] != '354':
            raise Exception('354 reply not received from server.')

        dateInfo = myFunction.getTime()
        msg = MIMEMultipart()
        msg['Date'] = dateInfo
        msg['From'] = self.userEmail
        msg['To'] = self.to_recipient
        msg['Cc'] = ', '.join(self.cc_list)
        msg['Bcc'] = ', '.join(self.bcc_list)
        msg['Subject'] = self.subject
        # Add body to email
        msg.attach(MIMEText(self.body, 'plain'))

        # Attach file------------------------------------------------------
        self.attachment_list = self.attachment_list.split(", ")
        if self.attachment_list != ['']:
            for attachment in self.attachment_list:
                # extract file name at the end of  path: "C:\Users\DELL\Desktop\test-attachment\test.txt"
                file_name = os.path.basename(attachment)
                file_path = attachment
                attachment = open(file_path, 'rb')

                body_part = MIMEBase('application', 'octet-stream')
                body_part.set_payload(attachment.read())
                encoders.encode_base64(body_part)
                # part = base64.b64encode(part)
                body_part.add_header('Content-Disposition', f'attachment; filename= {file_name}')
                msg.attach(body_part)
                attachment.close()

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
        self.clientSocket.close()

    def send_mail(self):
        try:
            # Connect server
            self.connect_server()
            # Send HELO command and print server response.
            self.send_helo_cmd()
            # Send MAIL FROM command and print server response.
            self.send_mailfrom_cmd()
            # Send RCPT TO command and print server response.
            self.send_rcpt_cmd()
            # Send DATA command and print server response.
            self.send_data_cmd()

            # Send QUIT command and print server response.
            self.send_quit_cmd()

        except Exception as e:
            print("Error occurred: ", e)
            print(traceback.format_exc())

        finally:

            print("Socket closed")


# ===========================================================================

mailserver = "127.0.0.1"
serverPort = 2225
serverAddr = (mailserver, serverPort)
clientAddr = "127.0.0.1"
clientMail = "codingAkerman@fit.hcmus.edu.vn"

# mailList
# mail1@gmail.com
# mail2@gmail.com
# mail3@gmail.com

# Create socket called clientSocket and establish a TCP connection with mailserver

# client = SMTPCLIENT(clientMail,"codingAkerman@fit.hcmus.edu.vn",
#                 "","",
#                 "test new mail " + input("Number:"), "2 txt file","txtattach.txt, txtattach2.txt")
# client.send_mail()
