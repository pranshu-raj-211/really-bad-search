from db.database import videos_collection
from utils.log_config import logger


def save_records(records: list):
    """Save multiple video records to the database.

    Duplicate records are ignored (upsert behavior).
    """
    if not records:
        return
    try:
        videos_collection.insert_many(
            records, ordered=False  # Ignore duplicates
        )
    except Exception as e:
        logger.exception(f"Error saving records: {e}")
