from datetime import datetime
from typing import Optional
import datetime

import pydantic

class FileSource(pydantic.BaseModel):
    hash: str
    file_path: str
    created_at: Optional[datetime.datetime] = datetime.datetime.utcnow()
    # total_frames: int = 0
    source_type: str # video or image