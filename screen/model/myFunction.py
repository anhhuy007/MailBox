import socket
import datetime
import json
import email
import base64
import os
import shutil


# smtp file

def getTime():
    now = datetime.datetime.now()
    today = datetime.date.today()
    ans = now.strftime("%H:%M:%S") + " " + today.strftime("%d/%m/%Y")
    return ans


def toInfoProccess(method, listRecipient):
    methodMsg = "SendMethod: " + method + "\r\n"
    recipientData = ""
    for i in range(0, len(listRecipient)):
        recipientData += listRecipient[i] + "\r\n"

    finalMsg = methodMsg + "To: \r\n" + recipientData
    return finalMsg


# pop3 file
# format file name yyyymmddhhmmss
def getFileName(timeInfo):
    timeInfo = timeInfo.split(" ")
    time = timeInfo[0].split(":")
    date = timeInfo[1].split("/")
    fileName = date[2] + date[1] + date[0] + time[0] + time[1] + time[2]
    return fileName


def save_mail(parsed_email, user_email):
    try:
        file_list = []
        attach = {}
        # mail to pypthon dictionary

        dataDict = {}
        dataDict["id"] = getFileName(parsed_email['Date'])
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
            # attach file
            elif part.get_content_type() == 'application/octet-stream':
                file_name = part.get_filename()
                attach["name"] = file_name
                file_type = file_name[file_name.find("."):]
                attach["type"] = file_type

                print(f"attachment name : {file_name}")
                # payload
                file_content = part.get_payload(decode=True)
                file_content_str = base64.b64encode(
                    file_content).decode()  # Convert bytes to base64 string, b64 decode to use
                attach["content"] = file_content_str
                file_list.append(attach.copy())  # the copy() method returns a shallow copy of the dictionary.
                attach.clear()

        dataDict["file_num"] = len(file_list)
        dataDict["file_list"] = file_list
        dataDict["seen"] = 0
        dataDict["file_saved"] = 0
        # save File
        save_mail_folder = os.path.join(os.path.dirname(__file__), '..', '..') + "\\mailBox\\"
        save_mail_path = save_mail_folder + getFileName(dateInfo) + ".json"
        # print (save_mail_path + "====================================")
        outputFile = open(save_mail_path,"w")
        json.dump(dataDict,outputFile,indent= 6)
        outputFile.close()
        filter_config_path = init_user_email_box(user_email)
        folder_path = get_folder_path(dataDict["subject"], dataDict["sender"], dataDict["body"], filter_config_path, user_email)
        move_mail(save_mail_path, folder_path)

    except Exception as e:
        print(f"Error occurred: {e}")
        return False
    return True

def save_attach(file_path):
    try:
        file_path = os.path.join(os.path.dirname(__file__), '..', '..') + "\\mailBox\\" + file_name + '.json'
        dataDict = json.load(open(file_path))
        file_list = dataDict["file_list"]
        dateInfo = dataDict["date"]
        for i in range(0, dataDict["file_num"]):
            file_name = file_list[i]["name"]
            file_type = file_list[i]["type"]
            file_content = file_list[i]["content"]
            save_file_path = destination_path + "\\" + file_name
            # open and write file ("wb")
            file_content = base64.b64decode(file_content)
            with open(save_file_path, 'wb') as f:
                f.write(file_content)
            print(f"--------------File {file_name} saved in {save_file_path}.------------")

    except Exception as e:
        print(f"Error occurred: {e}")
        return False
    return True


def seen_mail(file_name):
    try:
        file_path = os.path.join(os.path.dirname(__file__), '..', '..') + "\\mailBox\\" + file_name + '.json'
        dataDict = json.load(open(file_path))
        dataDict["seen"] = 1
        outputFile = open(file_path, "w")
        json.dump(dataDict, outputFile, indent=6)
        outputFile.close()
    except Exception as e:
        print(f"Error occurred: {e}")
        return False
    return True


# ////////////////////////////////////////////////////////////////////////
def init_user_email_box(user_name):
    user_folder = user_folder = os.path.join(os.path.dirname(__file__), '..', '..') + "\\Filter\\" + user_name+ "\\"
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    sub_folders = ["Important", "Project", "Work", "Spam"]
    for folder in sub_folders:
        folder_path = os.path.join(user_folder, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    filter_config_path = os.path.join(user_folder, 'config.json')
    json_content = {
        "From": {
            "from": ["ahihi@testing.com", "ahuu@testing.com"],
            "to_folder": "Project"
        },
        "Subject": {
            "subject": ["urgent", "ASAP"],
            "to_folder": "Important"
        },
        "Content": {
            "content": ["report", "meeting"],
            "to_folder": "Work"
        },
        "Spam": {
            "spam": ["virus", "hack", "crack"],
            "to_folder": "Spam"
        }
    }

    with open(filter_config_path, 'w') as json_file:
        json.dump(json_content, json_file, indent=4)

    return filter_config_path


# ////////////////////////////////////////////////////////////////////////
def move_mail(mail_path, folder_path):
    file_name = os.path.basename(mail_path)
    if os.path.exists(folder_path + file_name):
        return False
    shutil.copy(mail_path, folder_path + file_name)
    return True


def get_folder_path(subject, sender, body, json_file_path, user_email):
    if not os.path.exists(json_file_path):
        return "Spam"
    else:
        with open(json_file_path) as json_file:
            filters = json.load(json_file)

    subject = subject.lower()
    body = body.lower()
    sender = sender.lower()
    folder_name = "Spam"
    for key in filters["From"]["from"]:
        if key.lower() in sender:
            folder_name = filters["From"]["to_folder"]
            break
    for key in filters["Subject"]["subject"]:
        if key.lower() in subject:
            folder_name = filters["Subject"]["to_folder"]
            break
    for key in filters["Content"]["content"]:
        if key.lower() in body:
            folder_name = filters["Content"]["to_folder"]
            break
    for key in filters["Spam"]["spam"]:
        if key.lower() in subject or key in body:
            folder_name = filters["Spam"]["to_folder"]
            break
    
    filter_path = os.path.join(os.path.dirname(__file__), '..', '..', "Filter", user_email, folder_name) + "\\"
    return filter_path
