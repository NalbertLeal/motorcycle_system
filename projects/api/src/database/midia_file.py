from datetime import datetime

def new_media_file(
    file_path: str,
    file_type: str = 'video'
):
    '''
    PARAMETERS:
        file_type: str
            default = 'video'
            The acceptable values are 'video' or 'image'
    '''
    return {
        'path': file_path,
        'file_type': file_type,
        'created_at': datetime.now(),
    }