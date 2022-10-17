from xml.etree.ElementInclude import include
import pymongo
import os
import bcrypt
import string

# connect to mongo cluster 
mongopass = os.environ.get("MONGO_SNOW_DAY_PASSWORD")  
#with open("C:/Important Keys/mongouri.txt") as f: 
#    cluster = pymongo.MongoClient(f.read(), 27017)
client = pymongo.MongoClient("localhost", 27017)
db = client.local
#db = cluster["usercluster"]
collection = db["users"]
phonecoll = db["phonenums"]

salt = bcrypt.gensalt()

# return True when user exists and password is correct
def auth(phone: str, password: bytes):
    try:
        #find user by phone num
        user = collection.find_one({"phone": phone})
        # remove first 2 letters and last letter because password stored as b'$2b$12$yIdSkUl3U1GJm.wHPe9FfOoycD9B8C1v9cyUIKiZmRjDD8N8gSPS6'
        # encode to check
        hashedpw = user["password"][2:-1].encode("utf-8")       # Func will throw TypeError when user returns with None
        if bcrypt.checkpw(password, hashedpw):
            return True
        else:
            return False
    except TypeError:
        print("User gave invalid phone number")

def create(name: str, phone: str, zone: str, password: str):        # Return with any errors or return True when created and False when already exists

    # Make sure all args are valid

    for i in name:
        if i not in string.printable:
            return "Invalid Name"
    for i in phone:
        if i not in "1234567890":
            return "Invalid Phone Number"
    if zone.lower() not in ["north", "west", "central", "south", "muskoka"]:
        return "Invalid Zone"
    for i in password:
        if i not in string.printable:
            return "Invalid Password"
            
    if collection.find_one({"phone":  phone}) == None:
        password = bcrypt.hashpw(password.encode("utf-8"), salt)
        user = [{
            "phone": phone,
            "name": name.title(),
            "zone": zone,
            "password": str(password)
        }]
        collection.insert_many(user, ordered=False)
        return True
    else:
        return False

def getuser(phone: str, includepass: bool):     # Returns a python dict of user info
    user = collection.find_one({"phone": phone})
    user["_id"] = None      # Replace mongodb Objectid() with None to allow to become iterable
    user.pop("_id")
    if not includepass:
        user.pop("password")    # Remove storing of password for security
    return user

def zoneanduser():
    userlist = []
    for user in collection.distinct("phone"):
        userlist.append(getuser(user, includepass=False))
    return userlist

def delete(toRemove):
    collection.find_one_and_delete({'phone': toRemove})