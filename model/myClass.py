import base64
import random
import string
import os
import traceback


# ATTACHMENT ONLY
class ATTACHMENT:
    def __init__(self, content_type, file_name,transfer_encoding = "base64"):
        self.content_type = content_type #application/pdf or plain/text
        self.file_path = os.path.join(os.path.dirname(__file__), '..','test-attachment', '{}'.format(file_name))
        self.transfer_encoding = transfer_encoding # base64 or 7bit

    def header_format(self):
        header = ""
        header += "Content-Type: {}; charset=UTF-8; name= {}\r\n".format(self.content_type, self.file_path)
        header += "Content-Disposition: attachment; filename= {}\r\n".format(self.file_path)
        header += "Content-Transfer-Encoding: {}\r\n".format(self.transfer_encoding)
        header += "\r\n" # blank line
        return header.encode()
    def file_content(self):
        try:
            if(self.content_type[0:5] == "text/"):
                file = open(self.file_path, "r",encoding='utf-8')
            else : 
                file = open(self.file_path, "rb",encoding='utf-8')

            file_content = file.read()
            # print(file_content)
            file.close()
        except Exception as e:
            print(traceback.format_exc())
            print(e)
        
        file_content_encode = file_content.encode()
        file_content_encode_base64 = base64.b64encode(file_content_encode)
        return file_content_encode_base64
    
    def final_data(self):
        header_data  = self.header_format()
        file_content = self.file_content()
        final_msg = header_data + file_content
        return final_msg
    


# CONTENT HANDLE TEXT ONLY
class MAILCONTENT:


    def __init__(self,sender, to ,cc, bcc, date,subject,content, ATTACHMENT_LIST):
        self.sender = sender
        self.to = to # input list convert to string
        self.cc = cc # input list convert to string
        self.bcc = bcc # input list convert to string
        self.date = date
        self.subject = subject
        self.content = content
        self.ATTACHMENT_LIST = ATTACHMENT_LIST
        self.boundary = self.create_boundary()


    def header_format(self):
        header = ""
        
        header += "Content-Type: multipart/mixed; boundary=\"" + self.boundary + "\"\r\n"
        header += "Date: {}\r\n".format(self.date)
        header += "MIME-Version: 1.0\r\n"

        header += "User-Agent: Mozilla Thunderbird\r\n"
        header += "Content-Language: vi-x-KieuCu.[Chuan]\r\n"
        
        header += "To: {}\r\n".format(self.to)
        header += "From: {}\r\n".format(self.sender)
        header += "Subject: {}\r\n".format(self.subject)
        if self.cc != "":
            header += "Cc: {}\r\n".format(self.cc)
        if self.bcc != "":
            header += "Bcc: {}\r\n".format(self.bcc)
        

        
        header += "\r\n"
        header += "This is a multi-part message in MIME format.\r\n"
        return header.encode()

    def content_format(self):
        content = ""
        content += "Content-Type: text/plain; charset=UTF-8; format=flowed\r\n"
        content += "Content-Transfer-Encoding: 7bit\r\n"
        content += "\r\n"
        content += self.content + "\r\n" + "\r\n"
        return content.encode()

    def create_boundary(self,length=24):
        letters = string.ascii_letters
        result_str = ''.join(random.choice(letters) for i in range(length))
        return "------------" + result_str
    
    def add_boundary(self , decoded_content):
        return (self.boundary + "\r\n").encode() + decoded_content
    
    def add_close_boundary(self,decoded_content):
        return decoded_content + ("\r\n" + "\r\n" + self.boundary + "--\r\n"+ "\r\n.\r\n").encode()



    def final_data(self):
        # header
        final_data = self.header_format()
        # content
        final_data += self.add_boundary(self.content_format())

        # attachment0
        #...
        for attachment in self.ATTACHMENT_LIST:
            final_data += self.add_boundary(attachment.final_data())

        # close boundary
        final_data = self.add_close_boundary(final_data)
        return final_data


