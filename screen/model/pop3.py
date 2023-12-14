import socket
import json
import myFunction
import email
import os


class POP3CLIENT:
    port = 3335
    server = "127.0.0.1"
    serverAddr = (server, port)
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # # userEmail = "codingAkerman@fit.hcmus.edu.vn"

    mail_curr_index = 0
    mail_prev_index = 0
    filter_config_path = ""

    def __init__(self, user_email, password):
        self.userEmail = user_email
        self.password = password

    def connect_server(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Establish contact to pop3 server {} at port {}".format(self.server, self.port))
        self.clientSocket.connect(self.serverAddr)
        # check connect fail
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
        #handle error
        print(recv)
        if recv[0:3].lower() == '-err':
            raise Exception('Negative response from server. Stop program')
        self.mail_curr_index = recv.split(" ")[1]
        print("----------Mail current index: ", self.mail_curr_index)

        # open file
        self.filter_config_path = myFunction.init_user_email_box(self.userEmail)  # init user email box
        # read prev index------------------------------------------------
        open_file = open(self.filter_config_path, "r+")
        data = json.load(open_file)
        self.mail_prev_index = data["mail_index"]
        data["mail_index"] = self.mail_curr_index  # update mail index
        if self.mail_prev_index > self.mail_curr_index:
            print("------------------------adjust file config index")
        print("----------Mail prev index: ", self.mail_prev_index)
        open_file.seek(0)  # go to the beginning of the file
        json.dump(data, open_file, indent=6)
        # Truncate the file to remove any remaining content
        open_file.truncate()
        open_file.close()

    def send_list_cmd(self):
        listCmd = "LIST\r\n"
        self.clientSocket.send(listCmd.encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)
        if recv[0:3].lower() == '-err':
            raise Exception('Negative response from server. Stop program')

    def send_retr_cmd(self):
        for index in range(int(self.mail_prev_index) + 1, int(self.mail_curr_index) + 1):
            retrCmd = "RETR {}\r\n".format(index)
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
            dateInfo = parsed_email['date']

            # save mail
            if myFunction.save_mail(parsed_email, self.userEmail, self.filter_config_path):
                print("Save mail success")
            else:
                print("Save mail fail")

            # if(input("Do you want to save attach file in this mail ? (y/n) : ").lower() == "y"):
            #     if(myFunction.save_attach("mailBox\\"+ myFunction.getFileName(dateInfo) + ".json")):
            #         print("Save attach success")
            #     else:
            #         print("Save attach fail")

    def send_quit_cmd(self):
        # QUIT
        quitCmd = "QUIT\r\n"
        self.clientSocket.send(quitCmd.encode())
        print("Close connection")

    def run_pop3(self):
        try:
            # Connect server
            self.connect_server()
            # USER
            self.send_user_cmd()
            # PASS
            self.send_pass_cmd()
            # STAT
            self.send_stat_cmd()
            # LIST
            self.send_list_cmd()
            # RETR
            self.send_retr_cmd()
            # QUIT
            self.send_quit_cmd()
        except Exception as e:
            print("Error occurred: ", e)
            return False, e
        finally:
            self.clientSocket.close()
            print("close server")
        return True, "Run pop3 success"

# //----------------------------------------------------------------------
