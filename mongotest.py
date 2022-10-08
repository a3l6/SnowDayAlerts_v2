import pymongo
client = pymongo.MongoClient("localhost", 27017)
db = client.local

userinfo = [
    {"name": "Emilio Menddsdsdsdoza",
    "age": 11215,
    "gender": "mdfsfsdfale",
    "phone": "18002sdsds62001",
    "email": "noreply@sdsdsdgmail.com"}
]
db.users.insert_many(userinfo, ordered=False)

#print(db.users.find_one({"name": "Emilio Mendoza"}))

#for item in db.users.find().sort("x", pymongo.ASCENDING):
#    print(item)
