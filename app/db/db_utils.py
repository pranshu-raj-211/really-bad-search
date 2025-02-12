from db.database import videos
from utils.log_config import logger


def save_records(records: list):
    """Save multiple video records to the database.

    Duplicate records are ignored (upsert behavior).
    """
    if not records:
        return
    try:
        operations = [
            {
                "update_one": {
                    "filter": {"video_id": record["video_id"]},
                    "update": {"$set": record},
                    "upsert": True
                }
            }
            for record in records
        ]
        videos.bulk_write(operations)
        logger.debug("Saved records to videos collection")
    except Exception as e:
        logger.exception(f"Error saving records: {e}")


def get_paginated_videos(page: int = 1, page_size: int = 10):
    """Fetch videos from the database, in a paginated manner."""
    skip = (page - 1) * page_size
    
    cursor = videos.find()
    total = videos.count_documents({})
    
    video_list = list(cursor.sort("published_datetime", -1).skip(skip).limit(page_size))
    
    return {
        "items": video_list,
        "total": total,
        "page": page,
        "page_size": page_size
    }