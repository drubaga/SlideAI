from pydantic import BaseModel
from typing import List, Optional

class Slide(BaseModel):
    heading: str
    bullet_points: List[str]
    key_message: Optional[str] = None  # optional field

class Presentation(BaseModel):
    title: str
    slides: List[Slide]
