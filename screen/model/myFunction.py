
import socket
import datetime
import json
import email
import base64
import os
import shutil
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


def save_mail(parsed_email, user_email):
    try:
        file_list = []
        attach = {}
        # mail to pypthon dictionary
        
        dataDict = {}

        dataDict["user_email"] = user_email
        dateInfo = parsed_email['date']
        dataDict["date"] = parsed_email['date']
        dataDict["sender"] = parsed_email['sender']
        dataDict["to"] = parsed_email['to']
        dataDict["cc"] = parsed_email['cc']
        dataDict["bcc"] = parsed_email['bcc']
        dataDict["subject"] = parsed_email['subject']

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
                #payload
                file_content = part.get_payload(decode=True)
                file_content_str = base64.b64encode(file_content).decode()  # Convert bytes to base64 string, b64 decode to use
                attach["content"] = file_content_str
                file_list.append(attach.copy()) # the copy() method returns a shallow copy of the dictionary.
                attach.clear()

        dataDict["file_num"] = len(file_list)
        dataDict["file_list"] = file_list
        dataDict["seen"] = 0
        dataDict["file_saved"] = 0
        # save File
        save_mail_path =   'mailBox/' + getFileName(dateInfo)+ ".json"
        # print (save_mail_path + "====================================")
        outputFile = open(save_mail_path,"w")
        json.dump(dataDict,outputFile,indent= 6)
        outputFile.close()

        folder_name = filter_from_json(dataDict["subject"], dataDict["sender"], dataDict["body"],  user_email + "/config.json")
        move_mail_to_folder(user_email, folder_name, save_mail_path)
    except Exception as e:
        print(f"Error occurred: {e}")
        return False
    return True

def save_attach(file_path):
    try:
        dataDict = json.load(open(file_path))
        file_list = dataDict["file_list"]
        dateInfo = dataDict["Date"]
        for i in range(0,dataDict["file_num"]):
            file_name = file_list[i]["name"]
            file_type = file_list[i]["type"]
            file_content = file_list[i]["content"]
            save_file_path = "mailBox\\" + getFileName(dateInfo) + file_name
            # open and write file ("wb")
            file_content = base64.b64decode(file_content)
            with open(save_file_path, 'wb') as f:
                f.write(file_content)
            print(f"--------------File {file_name} saved in {save_file_path}.------------")

    except Exception as e:
        print(f"Error occurred: {e}")
        return False
    return True





#////////////////////////////////////////////////////////////////////////
def move_mail_to_folder(user_name,subject,sender,body,email_path,attachment_path):
    json_file_path = "mailBox/" + user_name + "/config.json"
    try:
        with open(json_file_path, 'r') as json_file:
            filters = json.load(json_file)
    except FileNotFoundError:
        return "Other"

    folder_name = "Other"

    for rule in filters.get("Filter", []):
        conditions = []

        if 'From' in rule:
            conditions.append(sender in rule['From'])

        if 'Subject' in rule:
            conditions.append(any(keyword in subject for keyword in rule['Subject']))

        if 'Content' in rule:
            conditions.append(any(keyword in body for keyword in rule['Content']))

        if 'Spam' in rule:
            conditions.append(any(keyword in subject or keyword in body for keyword in rule['Spam']))

        if all(conditions):
            folder_name = rule.get("To_folder", "Other")
            break
    try:
        folder_path = "mailBox/" + user_name + "/" + folder_name
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        shutil.move(email_path, folder_path)
        return True
    except Exception as e:
        print(f"Error occurred: {e}")
        return False
    
    if(os.path.isfile(attachment_path)):
        try:
            folder_path = "mailBox/" + user_name + "/" + "Attachment"
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                
            shutil.move(attachment_path, folder_path)
            return True
        except Exception as e:
            print(f"Error occurred: {e}")
            return False

def create_json_filter(user_mail):
    user_folder_path = os.path.join('mailBox', user_mail)
    if not os.path.exists(user_folder_path):
        os.makedirs(user_folder_path)

    json_file_path = os.path.join(user_folder_path, 'config.json')

    if not os.path.exists(json_file_path):
        json_content = {
            "filter": [
                {
                    "from": ["ahihi@testing.com", "ahuu@testing.com"],
                    "to_folder": "Project"
                },
                {
                    "subject": ["urgent", "ASAP"],
                    "to_folder": "Important"
                },
                {
                    "content": ["report", "meeting"],
                    "to_folder": "Work"
                },
                {
                    "spam": ["virus", "hack", "crack"],
                    "to_folder": "Spam"
                }
            ]
        }

        with open(json_file_path, 'w') as json_file:
            json.dump(json_content, json_file, indent=4)

    return json_file_path

def filter_from_json(subject, sender, body, json_file_path):
    try:
        with open(json_file_path, 'r') as json_file:
            filters = json.load(json_file)
    except FileNotFoundError:
        return "Other"

    folder_name = "Other"

    if(filters["filter"]):
        for filter in filters["filter"]:
            if("sender" in filter):
                for from_filter in filter["sender"]:
                    if(from_filter in sender):
                        folder_name = filter["to_folder"]
                        break
            if("subject" in filter):
                for subject_filter in filter["subject"]:
                    if(subject_filter in subject):
                        folder_name = filter["to_folder"]
                        break
            if("content" in filter):
                for content_filter in filter["content"]:
                    if(content_filter in body):
                        folder_name = filter["to_folder"]
                        break
            if("spam" in filter):
                for spam_filter in filter["spam"]:
                    if(spam_filter in subject or spam_filter in body):
                        folder_name = filter["to_folder"]
                        break
    return folder_name