from datetime import datetime
from typing import Tuple

def new_plate_content(
    processing_id: str,
    plate_id: str,
    frame_number: int,
    content: str
):
    '''
    PARAMETERS:
    '''
    return {
        'processing_id': processing_id,
        'plate_id': plate_id,
        'frame_number': frame_number,
        'content': content,
        'created_at': datetime.now()
    }