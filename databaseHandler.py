import pymongo
import os
import bcrypt

mongopass = os.environ.get("MONGO_SNOW_DAY_PASSWORD")
cluster = pymongo.MongoClient(f"mongodb+srv://admin:{mongopass}@snowdayalertscluster.olpm162.mongodb.net/?retryWrites=true&w=majority", 27017)
db = cluster["usercluster"]
collection = db["users"]



# get user profile
# match up passwords
# return true or false
def auth(phone: str, password):
    user = collection.find_one(phone)
    

def create():
    pass