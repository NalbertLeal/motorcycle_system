import os

from fastapi import APIRouter, HTTPException

from mongodb_lib import connection, collection, query

MONGO_HOST = os.environ.get('MONGO_HOST', default='localhost')
MONGO_PORT = os.environ.get('MONGO_PORT', default='27017')
MONGO_USER = os.environ.get('MONGO_USER', default='root')
MONGO_PASS = os.environ.get('MONGO_PASS', default='231564')

router = APIRouter(
    prefix="/source",
    tags=["source"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"message": "Not found"}},
)

@router.get('/list')
async def get_all_sources():
    try:
        conn = connection.create_connection(
            MONGO_HOST,
            MONGO_PORT,
            MONGO_USER,
            MONGO_PASS
        )
        media_files_coll = collection.access_collection(
            conn,
            'motor_detection_system',
            'media_files'
        )
        return query.get_all(media_files_coll)
    except:
        raise HTTPException(500, 'Internal error')

@router.get('/id/{source_id}')
async def get_source_by_id(source_id: str):
    try:
        conn = connection.create_connection(
            MONGO_HOST,
            MONGO_PORT,
            MONGO_USER,
            MONGO_PASS
        )
        media_files_coll = collection.access_collection(
            conn,
            'motor_detection_system',
            'media_files'
        )
        return query.get_by_id(media_files_coll, source_id)
    except:
        raise HTTPException(500, 'Internal error')

# @router.get('/hash/{file_hash}')
# async def get_source_by_file_hash(file_hash: str):
#     try:
#         source_collection = mongodb.access_collection(
#             'video_processing',
#             'sources'
#         )
#         return mongodb.get_by_hash(source_collection, file_hash)
#     except:
#         raise HTTPException(500, 'Internal error')