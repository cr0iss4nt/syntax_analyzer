from pydantic import BaseModel
from typing import List, Tuple

class ExportData(BaseModel):
    analysis: List[Tuple]
    entities: List[Tuple]
