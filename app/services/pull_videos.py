import asyncio
import httpx
from app.constants import LIST_API_URL, SEARCH_TERM, MAX_FETCH_RESULTS, FETCH_INTERVAL
from utils.load_env_vars import youtube_api_keys
from utils.log_config import logger
from datetime import datetime, timezone, timedelta
from db.db_utils import save_records


class YoutubeFetchDaemon:
    def __init__(self):
        self.api_keys = youtube_api_keys
        self.key_generator = self._create_key_generator()
        self.current_key = next(self.key_generator)
        self.fetch_interval = FETCH_INTERVAL
        self.is_active = False

    def _create_key_generator(self):
        """Generator to cycle through available API keys."""
        while True:
            for key in self.api_keys:
                yield key

    def _get_next_key(self):
        """Rotate to next api key."""
        self.current_key = next(self.key_generator)
        logger.debug("Quota exceeded, switched to next API key.")

    async def fetch_youtube_videos(self):
        """Fetch videos from youtube api."""
        params = {
            "part": "snippet",
            "q": SEARCH_TERM,
            "type": "video",
            "order": "date",
            "maxResults": MAX_FETCH_RESULTS,
            "publishedAfter": (
                datetime.now(timezone.utc) - timedelta(minutes=10)
            ).isoformat(),
            "key": self.current_key,
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
                logger.info(f"Fetched and saved {len(records)} videos")
        except httpx.HTTPStatusError as e:
            if e.response.status_code in [403, 429]:
                self._get_next_key()  # Rotation needed
            logger.error(f"HTTP error while fetching videos: {e}")
        except Exception as e:
            logger.error(f"Error fetching videos: {e}")

    async def start_fetching(self):
        """Start fetching videos from youtube api in the background."""
        self.is_running = True
        while self.is_running:
            try:
                await self.fetch_youtube_videos()
                await asyncio.sleep(self.fetch_interval)
            except Exception as e:
                logger.error(f"Error in fetch loop: {e}")
                await asyncio.sleep(
                    self.fetch_interval // 5
                )  # Pause before retry, prevent server overload

    def stop_fetching(self):
        """
        Stop the continuous fetching process.

        Synchronous because I want things to stop in priority - fix api calls and db limits
        """
        self.is_running = False
