import pymongo
client = pymongo.MongoClient("localhost", 27017)
db = client.local

userinfo = [
    {"name": "Emilio Mendoza"},
    {"age": 15},
    {"gender": "male"},
    {"phone": "1800262001"},
    {"email": "noreply@gmail.com"}
]
#db.users.insert_many(userinfo, ordered=False)

for item in db.users.find().sort("x", pymongo.ASCENDING):
    print(item)
