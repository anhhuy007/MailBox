import socket
import datetime
import json

'mail1@gmail.com\r\nmail2@gmail.com\r\n'


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
# format file name yyyy:mm:dd:hh:mm:ss
def getFileName(timeInfo):
    timeInfo = timeInfo.split(" ")
    time = timeInfo[0].split(":")
    date = timeInfo[1].split("/")
    fileName = date[2] + date[1] + date[0] + time[0] + time[1] + time[2]
    return fileName


def saveMail(mailData, usereMail):
    try:

        # mail to pypthon dictionary

        # mailData =  "+OK 176\r\nFrom: <codingAkerman@fit.hcmus.edu.vn>\r\nSendMethod: 1\r\nTo: \r\nmail1@gmail.com\r\nmail2@gmail.com\r\nDate: 17:48:51 25/11/2023\r\nSubject: test standard format 1\r\nContent: \r\noijojojoi\r\n.\r\n"
        dataDict = {}
        startList = 0
        endList = 0
        dataDict["userMail"] = usereMail
        mailData = mailData.split("\r\n")

        for i in range(0, len(mailData)):
            if "from" in mailData[i].lower():
                dataDict["From"] = mailData[i].split(" ")[1]
            if "sendmethod" in mailData[i].lower():
                dataDict["SendMethod"] = mailData[i].split(" ")[1]
                startList = i + 2
            if "date" in mailData[i].lower():
                dataDict["Date"] = mailData[i].split(" ", 1)[1]
                dateInfo = dataDict["Date"]
                endList = i
            if "subject" in mailData[i].lower():
                dataDict["Subject"] = mailData[i].split(" ")[1]
            if "content" in mailData[i].lower():
                dataDict["Content"] = mailData[i + 1]

        dataDict["RecipientList"] = mailData[startList:endList]
        dataDict["Seen"] = 0

        print(json.dumps(dataDict, indent=6))

        # save File
        fileName = "mailBox\\" + getFileName(dateInfo) + ".json"
        outputFile = open(fileName, "a", encoding='utf-8')

        json.dump(dataDict, outputFile, indent=6)
        outputFile.close()
    except Exception as e:
        print(f"Error occurred: {e}")
        return False
    return True
