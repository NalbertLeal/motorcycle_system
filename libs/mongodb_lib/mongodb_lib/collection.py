import pymongo

def access_collection(client, db_name, collection_name):
    db = client[db_name]
    return db[collection_name]