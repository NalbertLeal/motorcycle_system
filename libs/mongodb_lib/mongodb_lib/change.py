import pymongo

def delete_all(collection):
    try:
        collection.delete_many({})
        return True
    except:
        return False

def insert_one(collection, obj):
    try:
        result = collection.insert_one(obj)
        return True, result.inserted_id
    except:
        return False, None