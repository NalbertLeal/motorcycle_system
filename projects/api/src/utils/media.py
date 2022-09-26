import datetime

from src.kafka import producer
from src.database import file_source, processing
from src.database import mongodb

# def start_produce_media(file_path, file_type):
#     file_hash = ''
#     media_source(file_path, file_type, file_hash)
#     media_processing(file_hash)
#     if file_type == 'video':
#         producer.send_video(file_path, file_hash)
#     elif file_type == 'image':
#         producer.send_image(file_path, file_hash)

# def media_source(file_path, file_type, file_hash):
#     new_source = file_source.FileSource(
#         hash= file_hash,
#         file_path= file_path,
#         created_at= datetime.datetime.now(),
#         source_type= file_type
#     )
#     sources_collection = mongodb.access_collection('video_processing', 'sources')
#     source = mongodb.get_by_hash(sources_collection, file_hash)
#     if source is None:
#         mongodb.create_source(sources_collection, new_source)

# def media_processing(file_hash):
#     new_processing = processing.Processing(
#         source_hash= file_hash,
#         started_at= datetime.now(),
#         frames_count= 0
#     )
#     # sources_collection = mongodb.access_collection('video_processing', 'sources')
#     # source = mongodb.get_by_hash(sources_collection, file_hash)
#     processing_collection = mongodb.access_collection('video_processing', 'sources')
#     mongodb.create_preprocessing(processing_collection, new_processing)