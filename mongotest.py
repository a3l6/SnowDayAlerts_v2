import pymongo
import os
import bcrypt
"""client = pymongo.MongoClient("localhost", 27017)
db = client.local"""


mongopass = os.environ.get("MONGO_SNOW_DAY_PASSWORD")  
with open("C:\Important Keys\mongodb.txt") as f: 
    cluster = pymongo.MongoClient(f"mongodb+srv://admin:{f.read()}@snowdayalertscluster.olpm162.mongodb.net/?retryWrites=true&w=majority", 27017)
db = cluster["usercluster"]
collection = db["users"]

userinfo = [
    {
    "phone": "1800262001",
    "name": "John Higgins",
    "zone": "North",
    "password": str(bcrypt.hashpw(b"password", bcrypt.gensalt()))
    }
]
collection.insert_many(userinfo, ordered=False)

#print(db.users.find_one({"name": "Emilio Mendoza"}))

#for item in db.users.find().sort("x", pymongo.ASCENDING):
#    print(item)
