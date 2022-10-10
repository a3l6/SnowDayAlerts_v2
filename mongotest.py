import pymongo
client = pymongo.MongoClient("localhost", 27017)
db = client.local

userinfo = [
    {"phone": "18002sdsds62001",
    "age": 11215,
    "gender": "mdfsfsdfale",
    "name": "Emilio Menddsdsdsdoza",
    "email": "noreply@sdsdsdgmail.com"}
]
db.users.insert_many(userinfo, ordered=False)

#print(db.users.find_one({"name": "Emilio Mendoza"}))

#for item in db.users.find().sort("x", pymongo.ASCENDING):
#    print(item)
