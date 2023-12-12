
import json
import os
import base64


# the json file where the output must be stored 

#format file name yyyymmddhhmmss
def getFileName(timeInfo):
    timeInfo = timeInfo.split(" ")
    time = timeInfo[0].split(":")
    date = timeInfo[1].split("/")
    fileName = date[2] + date[1] + date[0] + time[0] + time[1]+ time [2]
    return fileName


def toInfoProccess(method, listRecipent):
    methodMsg = "SendMethod: "+ method + "\r\n"
    recipentData = ""
    for i in range (0,len(listRecipent)):
        recipentData += listRecipent[i] + "\r\n"

    finalMsg = methodMsg + "To: \r\n" + recipentData


#Handle TO command (CC Bcc)
#sendMethod: cc
#To: eeee
#To: eeee
#...
def toCmdProcces(method):
    
    # index = input("Enter sendMethod:[0: 1 receipent][1: CC][2: Bcc]")
    
    if method == "CC" or "Bcc":
        recipentNum = input("Enter number of recipents: ")
        for i in range(1,recipentNum+1):
            recipient = input(f"Enter recipent {i}: ")
            sendMsg = "RCPT TO: {}\r\n".format(recipient)




# # Open a file for reading
# file_path = os.path.join(os.path.dirname(__file__), '..','test-attachment', 'txtattach.txt')
# file = open(file_path, 'r',encoding='utf-8')

# # Read the first line of the file
# line = file.readline()
 
# # Loop through the rest of the file and print each line
# while line:
#     print(line)
#     line = file.readline()
 
# # Close the file when you're done
# file.close()

# sample_string = "GeeksForGeeks is the best"
# # sample_string_bytes = sample_string.encode() 
# a = sample_string.encode() 
# b = base64.b64encode(a) 

# base64_string = b.decode() 
  
# print(f"Encoded string: {b}") 


# base64_bytes = base64_string.encode()
# a = sample_string_bytes.decode()
# a = base64_string.encode()
# b = base64.b64decode(a)

# print ("ans = ", b)

# list_str = "a"
# # list_str = ", ".join(list)
# list_str = list_str.split(", ")
# print(list_str)

# print (len(list_str))

# file_path = os.path.join(os.path.dirname(__file__), '..','..','test-attachment', '{}'.format(file_name))

def init_user_email_box(user_name):
    user_folder = os.path.join(os.path.dirname(__file__), '..', '..',"mailBox",user_name) + "\\"
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)



    filter_config_path = os.path.join(user_folder, 'config.json')

    config_dict = {}

    general_list = {
        "user_name": user_name,
        "password": "123",
        "mail_server": "127.0.0.1",
        "smtp_port": "2225",
        "pop3_port": "3335",
        "auto_load": "20"
    }
    filter_list = {
        "From": {
            "key": ["ahihi@testing.com", "ahuu@testing.com"],
            "to_folder": "Project"
        },
        "Subject": {
            "key": ["urgent", "ASAP"],
            "to_folder": "Important"
        },
        "Content": {
            "key": ["report", "meeting"],
            "to_folder": "Work"
        },
        "Spam": {
            "key": ["virus", "hack", "crack"],
            "to_folder": "Spam"
        }
    }
    config_dict["General"] = general_list
    config_dict["Filter"] = filter_list
    config_dict["mail_index"] = "0"


    for folder in filter_list:
        folder_path = os.path.join(user_folder, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    with open(filter_config_path, 'w') as json_file:
        json.dump(config_dict, json_file, indent=4)

    return filter_config_path