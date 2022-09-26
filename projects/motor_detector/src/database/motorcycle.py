from datetime import datetime
from typing import Tuple

def new_motorcycle(
    processing_id: str,
    frame_number: int,
    bbox: Tuple[Tuple[int, int], Tuple[int, int]],
    confidence: int
):
    '''
    PARAMETERS:
    '''
    return {
        'processing_id': processing_id,
        'frame_number': frame_number,
        'bbox': bbox,
        'bbox_confidence': confidence,
        'created_at': datetime.now()
    }