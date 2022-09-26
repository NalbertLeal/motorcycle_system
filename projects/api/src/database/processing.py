from datetime import datetime

def new_processing(
    file_id: str
):
    '''
    PARAMETERS:
    '''
    return {
        'file_id': file_id,
        'started_at': datetime.now(),
        'ended_at': None,
    }