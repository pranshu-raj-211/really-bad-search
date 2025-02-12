from pymongo import MongoClient, ASCENDING
from utils.load_env_vars import mongo_uri

DB_NAME = "youtube_data"
COLLECTION_NAME = "videos"

client = MongoClient(mongo_uri)
db = client[DB_NAME]
videos = db[COLLECTION_NAME]

# index on published_datetime for faster queries
videos.create_index([("published_datetime", ASCENDING)], unique=True)
videos.create_index([("video_id", 1)], unique=True)