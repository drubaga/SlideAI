from pydantic import BaseModel
from typing import List, Optional

class Slide(BaseModel):
    """A single presentation slide with heading, bullet points, and an optional key message."""
    heading: str
    bullet_points: List[str]
    key_message: Optional[str] = None 
    image_keywords: Optional[List[str]] = None  


class Presentation(BaseModel):
    """A presentation consisting of a title and a list of slides."""
    title: str
    slides: List[Slide]
    enable_images: Optional[bool] = False
    image_provider: Optional[str] = None  # "pexels" or "serpapi"
