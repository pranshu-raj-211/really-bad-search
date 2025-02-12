from pydantic import BaseModel
from datetime import datetime
from typing import Dict, List

class VideoSchema(BaseModel):
    """Data model for video.
    
    Params:
    - video_id (str): Provided by youtube.
    - title (str): Title of the video as in api response.
    - description (str): Video description.
    - published_datetime (datetime): Timestamp, use for pagination and ordering.
    - thumbnails (dict): links of thumbnails.
    """
    video_id: str
    title: str
    description: str
    published_datetime: datetime
    thumbnails: Dict

class PaginatedResponse(BaseModel):
    """Data model for response by our api.
    
    Params:
    - items (list): List of videos which are fetched.
    - total (int): Total number of videos in collection.
    - page (int): Current page number (use in pagination).
    - page_size (int): Number of videos on that page."""
    items: List[VideoSchema]
    total: int
    page: int
    page_size: int