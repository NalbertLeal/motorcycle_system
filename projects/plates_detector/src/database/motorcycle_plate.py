from datetime import datetime
from typing import Tuple

def new_motorcycle_plate(
    processing_id: str,
    motorcycle_id: str,
    frame_number: int,
    bbox: Tuple[Tuple[int, int], Tuple[int, int]],
    confidence: int,
    label: str
):
    '''
    PARAMETERS:
    '''
    return {
        'processing_id': processing_id,
        'motorcycle_id': motorcycle_id,
        'frame_number': frame_number,
        'bbox': bbox,
        'bbox_confidence': confidence,
        'box_label': label,
        'created_at': datetime.now()
    }