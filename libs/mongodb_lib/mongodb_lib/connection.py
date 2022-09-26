from logging import exception

import pymongo

def create_connection(host, port, user, password):
    try:
        uri = 'mongodb://'+user+':'+password+'@'+host+':'+port+'/'
        client = pymongo.MongoClient(uri)
        client.server_info() # throw an exception if not connected
        return client
    except exception as e:
        return None