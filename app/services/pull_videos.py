import celery
import httpx
from app.constants import LIST_API_URL, SEARCH_TERM
from utils.load_env_vars import youtube_api_keys

from datetime import datetime, timezone, timedelta
from db.db_utils import save_records

MAX_RESULTS = 50

def get_api_key():
    while True:
        for key in youtube_api_keys:
            yield key

api_key_gen = get_api_key()

async def fetch_youtube_videos():
    """
    Fetch videos from the YouTube API and save them to the database.
    """
    api_key = next(api_key_gen)
    params = {
        "part": "snippet",
        "q": SEARCH_TERM,
        "type": "video",
        "order": "date",
        "maxResults": MAX_RESULTS,
        "publishedAfter": (datetime.now(timezone.utc) - timedelta(minutes=10)).isoformat(),
        "key": api_key,
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(LIST_API_URL, params=params)
            response.raise_for_status()
            data = response.json()

            records = [
                {
                    "video_id": item["id"]["videoId"],
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                    "published_datetime": item["snippet"]["publishedAt"],
                    "thumbnails": item["snippet"]["thumbnails"],
                }
                for item in data.get("items", [])
            ]

            save_records(records)
            print(f"Fetched and saved {len(records)} videos.")
    except httpx.HTTPStatusError as e:
        print(f"HTTP error while fetching videos: {e}")
    except Exception as e:
        print(f"Error fetching videos: {e}")
