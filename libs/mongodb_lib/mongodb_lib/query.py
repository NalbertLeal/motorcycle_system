import pymongo

def get_all(collection):
    result = collection.find({})
    return list(result)

def get_by_id(collection, id: str):
    return collection.find_one({
        '_id': id
    })