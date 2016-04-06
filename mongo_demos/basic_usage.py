import pymongo

conn = pymongo.MongoClient()
db = conn.esi
info = db.test

a = {'name': 'youzipi', 'age': 12}

info.insert(a)
