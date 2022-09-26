import os

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile

from mongodb_lib import connection, collection, change

from src.utils import file as file_utils
from src.database import midia_file, processing
from src.kafka import producer

MONGO_HOST = os.environ.get('MONGO_HOST', default='localhost')
MONGO_PORT = os.environ.get('MONGO_PORT', default='27017')
MONGO_USER = os.environ.get('MONGO_USER', default='root')
MONGO_PASS = os.environ.get('MONGO_PASS', default='231564')

router = APIRouter(
    prefix="/media",
    tags=["media"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {'message': 'Not found'}},
)

# @router.get('/list')
# async def get_medias_list():
#     ...

# @router.get('/{media_frame}')
# async def get_media(media_frame: str):
#     ...

@router.post('/')
async def receive_media(file: UploadFile = File(...)):
    file_path = './medias_folder/'+file.filename
    try:
        # write file to disk
        contents = await file.read()
        with open(file_path, 'wb') as f:
            f.write(contents)
        # discover media file type
        file_type = file_utils.define_media_type(file.filename)
        if file_type == 'unknown':
            await file.close()
            return {
                'message': 'Media file with undefined type'
            }
        # register file
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
        new_media_file = midia_file.new_media_file(file_path, file_type)
        ok, media_file_id = change.insert_one(media_files_coll, new_media_file)
        if not ok:
            await file.close()
            return {"message": f"Internal server error"}
        # register processing
        processings_coll = collection.access_collection(
            conn,
            'motor_detection_system',
            'processings'
        )
        new_processing = processing.new_processing(media_file_id)
        ok, processing_id = change.insert_one(processings_coll, new_processing)
        if not ok:
            await file.close()
            return {"message": f"Internal server error"}
        # send frames to kafka
        if file_type == 'video':
            producer.send_video(file_path, processing_id)
        else:
            producer.send_image(file_path, processing_id)
        # finish
        await file.close()
        return {"message": f"Successfuly uploaded {file.filename}"}
    except Exception as e:
        await file.close()
        print(e)
        return {"message": "There was an error uploading the file"}