import json
from datetime import datetime

class FileAttachment:
    def __init__(self, name, type, content):
        self.name = name
        self.type = type
        self.content = content

class Email:
    def __init__(self, user_email, date, sender, to, cc, bcc, subject, body, file_num, file_list, seen, file_saved):
        self.user_email = user_email
        self.date = date
        self.sender = sender
        self.to = to
        self.cc = cc
        self.bcc = bcc
        self.subject = subject
        self.body = body
        self.file_num = file_num
        self.file_list = [FileAttachment(**file_data) for file_data in file_list]
        self.seen = seen
        self.file_saved = file_saved

    @classmethod
    def from_json(cls, json_string):
        data = json.loads(json_string)
        date = datetime.strptime(data["date"], "%H:%M:%S %d/%m/%Y")  # Convert date string to datetime object
        return cls(
            user_email=data["user_email"],
            date=date,
            sender=data["sender"],
            to=data["to"],
            cc=data["cc"],
            bcc=data["bcc"],
            subject=data["subject"],
            body=data["body"],
            file_num=data["file_num"],
            file_list=data["file_list"],
            seen=data["seen"],
            file_saved=data["file_saved"]
        )

# Example usage:
json_data = '''
{
  "user_email": "mail1@gmail.com",
  "date": "21:46:55 07/12/2023",
  "sender": "mail1@gmail.com",
  "to": "mail1@gmail.com",
  "cc": "",
  "bcc": "",
  "subject": "123456",
  "body": "123456",
  "file_num": 1,
  "file_list": [
    {
      "name": "txtattach.txt",
      "type": ".txt",
      "content": "VHLGsOG7nW5nIMSQSCBLSFROLCDEkEhRRy1IQ00gbMOgIHRydW5nIHTDom0gxJHDoG8gdOG6oW8gxJHhuqFpIGjhu41jLCBzYXUgxJHhuqFpIGjhu41jLCBjdW5nIGPhuqVwIG5ndeG7k24gbmjDom4gbOG7sWMsIMSR4buZaSBuZ8WpIGNodXnDqm4gZ2lhIHRyw6xuaCDEkeG7mSBjYW8gdHJvbmcgY8OhYyBsxKluaCB24buxYyBraG9hIGjhu41jIGPGoSBi4bqjbiwga2hvYSBo4buNYyBsacOqbiBuZ8OgbmgsIGtob2EgaOG7jWMgY8O0bmcgbmdo4buHIG3FqWkgbmjhu41uLCBjw7MgbsSDbmcgbOG7sWMgc8OhbmcgdOG6oW8sIGzDoG0gdmnhu4djIHRyb25nIG3DtGkgdHLGsOG7nW5nIGPhuqFuaCB0cmFuaCBxdeG7kWMgdOG6vzsgbMOgIG7GoWkgdGjhu7FjIGhp4buHbiBuaOG7r25nIG5naGnDqm4gY+G7qXUga2hvYSBo4buNYyDEkeG7iW5oIGNhbyB04bqhbyByYSBjw6FjIHPhuqNuIHBo4bqpbSB0aW5oIGhvYSDEkcOhcCDhu6luZyBuaHUgY+G6p3UgcGjDoXQgdHJp4buDbiBLSENOIHbDoCB5w6p1IGPhuqd1IHBow6F0IHRyaeG7g24ga2luaCB04bq/IC0geMOjIGjhu5lpIG5nw6B5IGPDoG5nIGNhbyBj4bunYSDEkeG6pXQgbsaw4bubYywgcGjDuSBo4bujcCB24bubaSB4dSB0aOG6vyBwaMOhdCB0cmnhu4NuIHRo4bq/IGdp4bubaS4NCsSQxrDhu6NjIGdp4bqjbmcgZOG6oXkgYuG7n2kgxJHhu5lpIG5nxakgR2nDoW8gc8awLCBQaMOzIGdpw6FvIHPGsCB2w6AgR2nhuqNuZyB2acOqbiBow6BuZyDEkeG6p3UgY8OzIHTDom0gaHV54bq/dCwgdOG6rW4gdMOibSB2w6AgZ2nhu49pIGNodXnDqm4gbcO0bg0KVGnhur9wIGPhuq1uIHbhu5tpIGPDoWMgY2jGsMahbmcgdHLDrG5oIMSRw6BvIHThuqFvIGPhuq1wIG5o4bqtdCwgaGnhu4duIMSR4bqhaSB2w6AgxJHhuqF0IGNodeG6qW4gcXXhu5FjIHThur8NCsSQxrDhu6NjIHBow6F0IHRyaeG7g24gdG/DoG4gZGnhu4duIGLhuqNuIHRow6JuIHThu6sgY8OhYyB0cuG6o2kgbmdoaeG7h20gaOG7jWMgdGh14bqtdCwgbmdoacOqbiBj4bupdSBraG9hIGjhu41jLCB0aOG7sWMgaMOgbmgsIHRo4buxYyB04bq/ICB04bqhaSBkb2FuaCBuZ2hp4buHcA=="
    }
  ],
  "seen": 0,
  "file_saved": 0
}
'''

# Deserialize the JSON string
# Deserialize the JSON string
email_object = Email.from_json(json_data)

# Accessing the attributes of the deserialized object
print(email_object.user_email)
print(email_object.date)
print(email_object.sender)
print(email_object.file_list[0].name)