from datetime import datetime
from typing import Tuple

def new_metric(
    frame_number: int,
    frame_received_at,
    pre_processing_time,
    segmentation_time,
    classification_time,
    frame_send_at=None,
):
    '''
    PARAMETERS:
    '''
    return {
        'frame_number': frame_number,
        'have_detections': frame_send_at is not None,
        'frame_received_at': str(frame_received_at),
        'pre_processing_time': str(pre_processing_time),
        'segmentation_time': str(segmentation_time),
        'classification_time': str(classification_time),
        'frame_send_at': str(frame_send_at)
    }