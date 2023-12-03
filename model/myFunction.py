
import socket
import datetime
import json
import email
import base64
#smtp file

def getTime():
    now = datetime.datetime.now()
    today = datetime.date.today()
    ans = now.strftime("%H:%M:%S") + " " + today.strftime("%d/%m/%Y")
    return ans

def toInfoProccess(method, listRecipient):
    methodMsg = "SendMethod: "+ method + "\r\n"
    recipientData = ""
    for i in range (0,len(listRecipient)):
        recipientData += listRecipient[i] + "\r\n"

    finalMsg = methodMsg + "To: \r\n" + recipientData
    return finalMsg








# pop3 file
#format file name yyyymmddhhmmss
def getFileName(timeInfo):
    timeInfo = timeInfo.split(" ")
    time = timeInfo[0].split(":")
    date = timeInfo[1].split("/")
    fileName = date[2] + date[1] + date[0] + time[0] + time[1]+ time [2]
    return fileName



def save_mail(in_data, user_email):
    try:
        file_list = []
        attach = {}
        # mail to pypthon dictionary
        parsed_email = email.message_from_string(in_data)
        dataDict = {}
        dataDict["user_email"] = user_email
        dateInfo = parsed_email['Date']
        dataDict["Date"] = parsed_email['Date']
        dataDict["From"] = parsed_email['From']
        dataDict["To"] = parsed_email['To']
        dataDict["Cc"] = parsed_email['Cc']
        dataDict["Bcc"] = parsed_email['Bcc']
        dataDict["Subject"] = parsed_email['Subject']

         # SAVE FILE
        for part in parsed_email.walk():
            if part.get_content_type() == 'text/plain':
                print(f"body content : {part.get_payload()}")
                dataDict["body"] = part.get_payload()
            #attach file
            elif part.get_content_type() == 'application/octet-stream':
                file_name = part.get_filename()
                attach["name"] = file_name
                file_type = file_name[file_name.find("."):]
                attach["type"] = file_type

                print(f"attachment name : {file_name}")
                
                if file_type == ".pdf" or file_type == ".jpeg" or file_type == ".png" or file_type == ".docx" or file_type == ".zip" :
                    file_content = part.get_payload(decode=True)
                    file_content_str = base64.b64encode(file_content).decode()  # Convert bytes to base64 string, b64 decode to use
                    attach["content"] = file_content_str
                    file_list.append(attach.copy()) # the copy() method returns a shallow copy of the dictionary.
                    attach.clear()
                    # with open(save_file_path, 'wb') as f:
                    #     f.write(file_content)
                    # print(f"--------------PDF file {file_name} saved.------------")
                if file_type == ".txt":
                    file_content = part.get_payload(decode=False)
                    file_content = file_content.encode()
                    file_content = base64.b64decode(file_content)
                    file_content = file_content.decode()
                    attach["content"] = file_content
                    file_list.append(attach.copy())
                    attach.clear()
                    # with open(save_file_path, 'w') as f:
                    #     f.write(file_content)

        dataDict["file_num"] = len(file_list)
        dataDict["file_list"] = file_list
        dataDict["seen"] = 0
        dataDict["file_saved"] = 0

        # print(json.dumps(dataDict,indent= 6))


        # save File
        save_mail_path = "mailBox\\"+ getFileName(dateInfo)+ ".json"
        outputFile = open(save_mail_path,"w")
        
        json.dump(dataDict,outputFile,indent= 6)
        outputFile.close()
    except Exception as e:
        print(f"Error occurred: {e}")
        return False
    return True

