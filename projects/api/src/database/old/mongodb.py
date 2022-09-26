import datetime
from logging import exception
import os
from typing import Any

import pymongo

from src.mongo_db import file_source, camera_source, processing

MONGO_HOST = os.environ.get('MONGO_HOST', default='127.0.0.1')
MONGO_PORT = os.environ.get('MONGO_PORT', default='27017')
MONGO_USER = os.environ.get('MONGO_USER', default='root')
MONGO_PASS = os.environ.get('MONGO_PASS', default='231564')

def create_connection(host, port, user, password):
    try:
        uri = 'mongodb://'+user+':'+password+'@'+host+':'+port+'/'
        client = pymongo.MongoClient(uri)
        client.server_info()
        return client
    except exception as e:
            print(e)

def access_collection(client, db_name, collection_name):
    db = client[db_name]
    return db[collection_name]

def get_all(collection):
    result = collection.find_all()
    return list(result)

def get_by_id(collection, id: str):
    return collection.find_one({
        '_id': id
    })

def get_by_hash(collection, hash: str):
    return collection.find_one({
        'hash': hash
    })

def create_source(collection, source):
    result = collection.insert_one({
        'hash': source.hash,
        'file_path': source.file_path,
        'created_at': source.created_at,
        'total_frames': source.total_frames, 
        'source_type': source.source_type
    })
    return result.inserted_id

def create_preprocessing(
    processing_collection,
    processing: processing.Processing
):
    """
    Create the new processing document into collection. It assume that
    the caller already veryfied if the processing source exists.
    """
    result = processing_collection.insert_one({
        'source_hash': processing.source_hash,
        'started_at': processing.started_at,
        'ended_at': processing.ended_at,
        'frames_count': processing.frames_count,
    })
    return result.inserted_id

def update_processing_ended_at(collection, processing_id: Any):
    collection.find_one_and_update({
            '_id': processing_id
        },
        {
            'ended_at': datetime.datetime.utcnow()
        }
    )

def update_processing_frames_count(collection, processing_id: Any, increase_by: int):
    collection.find_one_and_update({
            '_id': processing_id
        },
        {
            '$inc': {
                'frames_count': increase_by
            } 
        }
    )