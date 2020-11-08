import requests, sys
import xml.etree.ElementTree as ET
from time import strftime
import sys

# use with python ./test.py 0123456789 "Test message"
phone = sys.argv[1]
msg = sys.argv[2]

ip = "192.168.8.1" #Dongle ip

#Get token
r = requests.get("http://%s/api/webserver/token" % ip)
root = ET.fromstring(r.content)
token = root[0].text
print("token: {token}")

#Send sms
now_date = strftime("%Y-%m-%d %H:%M:%S")
headers = { "__RequestVerificationToken": token, "Content-Type": "text/xml" }
data = f"<request><Index>-1</Index><Phones><Phone>%s</Phone></Phones><Sca/><Content>%s</Content><Length>%d</Length><Reserved>1</Reserved><Date>{now_date}</Date></request>" % (phone, msg, len(msg))
print(f"data: {data}")
r = requests.post(f"http://{ip}/api/sms/send-sms", data=data, headers=headers)
print(f"sent-sms {r.headers} : {r.content}")
