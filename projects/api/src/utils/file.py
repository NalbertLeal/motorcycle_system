import hashlib
from logging import exception
import time

import cv2

VIDEOS_EXTENSIONS = ['mp4', 'avi', 'MP4', 'AVI']
IMAGES_EXTENSIONS = ['jpeg', 'png', 'jpg', 'JPEG', 'PNG', 'JPG']

def _open_video_file(file_path: str):
    video_reader = cv2.VideoCapture(file_path)

    if not video_reader.isOpened():
        raise exception('OpenCV cant open the video.')

    frames_number = video_reader.get(cv2.CAP_PROP_FRAME_COUNT)

    return video_reader, int(frames_number)

def _read_frame(video_reader):
    has_frame, frame = video_reader.read()
    
    if not has_frame:
        return None

    return frame

def read_video_frames(file_path: str):
    video_reader, frames_number  = _open_video_file(file_path)

    for frame_counter in range(frames_number):
        if video_reader.isOpened():
            frame = _read_frame(video_reader)
            if frame is None:
                yield None
            yield frame, frame_counter, frames_number
        else:
            yield None

def compute_file_hash(fiilepath: str):
    '''
    Compute the SHA256 file.
    PARAMETERS:
        filepath: str
            The path of the file to be used to generate the hash.
    '''
    BLOCK_SIZE = 65536
    file_hash = hashlib.sha256()
    with open(fiilepath, 'rb') as file:
        fb = file.read(BLOCK_SIZE)
        while len(fb) > 0:
            file_hash.update(fb)
            fb = file.read(BLOCK_SIZE)
    return file_hash.hexdigest()

def define_media_type(filename: str):
    extension = filename[-3:]
    if extension in VIDEOS_EXTENSIONS:
        return 'video'
    if extension in IMAGES_EXTENSIONS:
        return 'image'
    return 'unknown'