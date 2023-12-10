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

        dataDict["user_email"] = user_email
        dateInfo = parsed_email['Date']
        dataDict["date"] = parsed_email['Date']
        dataDict["from"] = parsed_email['From']
        dataDict["to"] = parsed_email['To']
        dataDict["cc"] = parsed_email['Cc']
        dataDict["bcc"] = parsed_email['Bcc']
        dataDict["subject"] = parsed_email['Subject']

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
                attach["link"] = ""

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
        save_mail_path = "D:\\MailBox\\mailBox\\" + getFileName(dateInfo) + ".json"
        outputFile = open(save_mail_path, "w")
        json.dump(dataDict, outputFile, indent=6)
        outputFile.close()
        filter(dataDict["Subject"], dataDict["From"], dataDict["body"], save_mail_path, user_email)
    except Exception as e:
        print(f"Error occurred: {e}")
        return False
    return True


def save_attach(file_path):
    try:
        dataDict = json.load(open(file_path))
        file_list = dataDict["file_list"]
        dateInfo = dataDict["Date"]
        for i in range(0, dataDict["file_num"]):
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


# ////////////////////////////////////////////////////////////////////////
def create_folder(user_name, folder_name, file_path):
    try:
        folder_path = "mailBox/" + user_name + "/" + folder_name
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        shutil.move(file_path, folder_path)
        return True
    except Exception as e:
        print(f"Error occurred: {e}")
        return False


def filter(subject, sender, content, file_path, user_name):
    if sender == "ahihi@testing.com" or sender == "ahuu@testing.com":
        folder_name = "Project"
    elif "urgent" in subject or "ASAP" in subject:
        folder_name = "Important"
    elif "report" in content or "meeting" in content:
        folder_name = "Work"
    elif "virus" in subject or "hack" in subject or "crack" in subject or "virus" in content or "hack" in content or "crack" in content:
        folder_name = "Spam"
    else:
        return "Other"

    if create_folder(user_name, folder_name, file_path):
        return f"To folder: {folder_name}"
    else:
        return "Failed to create folder or move file"
