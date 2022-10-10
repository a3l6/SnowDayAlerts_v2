import pymongo
import os
"""client = pymongo.MongoClient("localhost", 27017)
db = client.local"""


mongopass = os.environ.get("MONGO_SNOW_DAY_PASSWORD")  
with open("C:\Important Keys\mongodb.txt") as f: 
    cluster = pymongo.MongoClient(f"mongodb+srv://admin:{f.read()}@snowdayalertscluster.olpm162.mongodb.net/?retryWrites=true&w=majority", 27017)
db = cluster["usercluster"]
collection = db["users"]

userinfo = [
    {
        "phone": "7052294272",
        "password": "b'$2b$12$TBCziv/3H4fs31W.yr3jmeXG2eWIWemA5aHRZOTwYTAh6YC0nvwYy'"
    }
]
collection.insert_many(userinfo, ordered=False)

#print(db.users.find_one({"name": "Emilio Mendoza"}))

#for item in db.users.find().sort("x", pymongo.ASCENDING):
#    print(item)
