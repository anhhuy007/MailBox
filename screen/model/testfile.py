
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

list_str = "a"
# list_str = ", ".join(list)
list_str = list_str.split(", ")
print(list_str)

print (len(list_str))

