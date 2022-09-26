import os

from fastapi import APIRouter, HTTPException

from mongodb_lib import connection, collection, query

MONGO_HOST = os.environ.get('MONGO_HOST', default='localhost')
MONGO_PORT = os.environ.get('MONGO_PORT', default='27017')
MONGO_USER = os.environ.get('MONGO_USER', default='root')
MONGO_PASS = os.environ.get('MONGO_PASS', default='231564')

router = APIRouter(
    prefix="/processing",
    tags=["processing"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"message": "Not found"}},
)

@router.get('/list')
async def get_all_processings():
    try:
        conn = connection.create_connection(
            MONGO_HOST,
            MONGO_PORT,
            MONGO_USER,
            MONGO_PASS
        )
        processings_coll = collection.access_collection(
            conn,
            'motor_detection_system',
            'processings'
        )
        return query.get_all(processings_coll)
    except:
        raise HTTPException(500, 'Internal error')

@router.get('/id/{processing_id}')
async def get_processing_by_id(processing_id: str):
    try:
        conn = connection.create_connection(
            MONGO_HOST,
            MONGO_PORT,
            MONGO_USER,
            MONGO_PASS
        )
        processings_coll = collection.access_collection(
            conn,
            'motor_detection_system',
            'processings'
        )
        return query.get_by_id(processings_coll, processing_id)
    except:
        raise HTTPException(500, 'Internal error')

# @router.get('/hash/{file_hash}')
# async def get_processing_by_file_hash(file_hash: str):
#     try:
#         processing_collection = mongodb.access_collection(
#             'video_processing',
#             'processing'
#         )
#         return mongodb.get_by_hash(processing_collection, file_hash)
#     except:
#         raise HTTPException(500, 'Internal error')