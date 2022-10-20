import time
from twilio.rest import Client
import databaseHandler
from checker import check
import os
import schedule

with open("C:/Users/707011/Desktop/twillio_sid.txt") as f:
    acc_sid = f.read()
with open("C:/Users/707011/Desktop/twillio_auth.txt") as f:
    acc_auth = f.read()
with open("C:/Users/707011/Desktop/phonenum_twilio.txt") as f:
    twilionum = f.read()


#acc_sid = os.environ.get("twilio_sid")
#acc_auth = os.environ.get("twilio_auth")
#twilionum = os.environ.get("twilio_num")

client = Client(acc_sid, acc_auth)


def sendMessages():
    usersinfo = databaseHandler.zoneanduser()
    for user in usersinfo:
        if user["phone"] != "admin":
            message = client.messages.create(
                                    body= check(user["zone"]),
                                    from_=twilionum,
                                    to=user["phone"]
                                )

def main():
    schedule.every().day.at("06:30").do(sendMessages)
    #messaging.sendMessages()
    while 1:
        schedule.run_pending()
        time.sleep(2)

def send_admin_message(message: str):
    usersinfo = databaseHandler.zoneanduser()
    print(usersinfo)
    for user in usersinfo:
        if user["phone"] != "admin":
            message = client.messages.create(
                                            body= message,
                                            from_=twilionum,
                                            to=user["phone"]
                                        )