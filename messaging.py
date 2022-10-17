from operator import indexOf
import schedule
import time
from twilio.rest import Client
from databaseHandler import zoneanduser
from checker import check

with open("C:/Users/707011/Desktop/twillio_sid.txt") as f:
    acc_sid = f.read()
with open("C:/Users/707011/Desktop/twillio_auth.txt") as f:
    acc_auth = f.read()
client = Client(acc_sid, acc_auth)


def sendMessages():
    usersinfo = zoneanduser()
    for user in usersinfo:
        message = client.messages.create(
                                body= check(user["zone"]),
                                from_='+17059998264',
                                to=user["phone"]
                            )
def main():
    #schedule.every().day.at("10:30").do(sendMessages())
    sendMessages()
    while 1:
        schedule.run_pending()
        time.sleep(1)