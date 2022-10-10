import pymongo
import os
import bcrypt

# connect to mongo cluster 
mongopass = os.environ.get("MONGO_SNOW_DAY_PASSWORD")  
with open("C:\Important Keys\mongodb.txt") as f: 
    cluster = pymongo.MongoClient(f"mongodb+srv://admin:{f.read()}@snowdayalertscluster.olpm162.mongodb.net/?retryWrites=true&w=majority", 27017)
db = cluster["usercluster"]
collection = db["users"]

salt = bcrypt.gensalt()

def auth(phone: str, password: bytes):
    #find user by phone num
    user = collection.find_one({"phone": phone})
    # remove first 2 letters and last letter because password stored as b'$2b$12$yIdSkUl3U1GJm.wHPe9FfOoycD9B8C1v9cyUIKiZmRjDD8N8gSPS6'
    # encode to check
    hashedpw = user["password"][2:-1].encode("utf-8")
    if bcrypt.checkpw(password, hashedpw):
        return True
    else:
        return False

# get email
# store email
# hash pw
# store pw
def create(email: str, password: str):
    user = [{
        "phone": phone

    }]

"""
password = bcrypt.hashpw(b"password", salt)
userinfo = [
    {"phone": "18002672001",
    "password": str(password)}
]
db.users.insert_many(userinfo, ordered=False)"""