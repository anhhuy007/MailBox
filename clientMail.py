import socket
import datetime
import myFunction

msg = "\r\n"
endmsg = "\r\n.\r\n"



# Choose a mail server (e.g. Google mail server) and call it mailserver

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
print("Establist contact to mail server {} at port {}".format(mailserver,serverPort))
clientSocket.connect(serverAddr)

#check connect fail
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[0:3] != '220':
    print('220 reply not received from server. Stop program')

# Send HELO command and print server response.
heloCmd = "HELO [{}]\r\n".format(clientAddr)
clientSocket.send(heloCmd.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[0:3] != '250':
    print('250 reply not received from server.')






# Send MAIL FROM command and print server response.
mailFromCmd = "MAIL FROM: {}\r\n".format(clientMail)
clientSocket.send(mailFromCmd.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[0:4] != '250':
    print('250 reply not received from server.')


# Send RCPT TO command and print server response.
recipientList = []
recipentNum = 0
sendMethod = input("Enter sendmethod [0:normal][1:CC][2:Bcc]: ")
if sendMethod == "1" or sendMethod == "2":
    recipentNum = input("Enter number of recipents: ")
    for i in range(1,int(recipentNum)+1):
        recipient = input(f"Enter recipent {i}: ")
        recipientList.append(recipient)
        rcptToCmd = "RCPT TO: {}\r\n".format(recipient)
        clientSocket.send(rcptToCmd.encode())
        recv1 = clientSocket.recv(1024).decode()
        print(recv1)
        if recv1[0:3] != '250':
            print('250 reply not received from server.')
else :
    recipient = input(f"Enter recipent: ")
    recipientList.append(recipient)
    rcptToCmd = "RCPT TO: {}\r\n".format(recipient)
    clientSocket.send(rcptToCmd.encode())
    recv1 = clientSocket.recv(1024).decode()
    print(recv1)
    if recv1[0:3] != '250':
        print('250 reply not received from server.')

# rcptToCmd = "RCPT TO: {}\r\n".format(clientMail)
# clientSocket.send(rcptToCmd.encode())
# recv1 = clientSocket.recv(1024).decode()
# print(recv1)
# if recv1[0:3] != '250':
#     print('250 reply not received from server.')




# Send DATA command and print server response.
dataCmd = "DATA\r\n"
clientSocket.send(dataCmd.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[0:3] != '354':
    print('354 reply not received from server.')


#header information: FROM, TO, DATE, SUBJECT
fromInfo = "From: <{}>\r\n".format(clientMail)


# toInfo= "To: <{}>\r\n".format(clientMail)
toInfo  = myFunction.toInfoProccess(sendMethod,recipientList)


dateInfo = "Date: " + myFunction.getTime() + "\r\n"
subjectInfo = "Subject: {}\r\n".format(input("Enter Subject : "))
headerInfo = fromInfo + toInfo + dateInfo + subjectInfo
#  mail content
mailContent = "Content: \r\n" +  input ("Enter mail content : ")


# Message ends with a single period.
dataSend =  headerInfo  +mailContent + endmsg
print("------------------------dataSend = ",dataSend)
clientSocket.send(dataSend.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[0:3] != '250':
    print('250 reply not received from server.')


# Send QUIT command and get server response.
dataCmd = "QUIT\r\n"
clientSocket.send(dataCmd.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[0:3] != '221':
    print('221 reply not received from server.')


