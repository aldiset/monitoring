from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ResultItem(BaseModel):
    name: str
    value: str

class DataCreate(BaseModel):
    type: str
    framework_name: str
    specification: str
    result: List[ResultItem]
    created_at: Optional[datetime] = None
