from datetime import datetime
from typing import Optional
import datetime

import pydantic

class Processing(pydantic.BaseModel):
    source_hash: str
    started_at: Optional[datetime.datetime] = datetime.datetime.utcnow()
    ended_at: Optional[datetime.datetime]
    frames_count: int