import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query
from models.video_model import PaginatedResponse
from db.db_utils import get_paginated_videos
from services.pull_videos import YoutubeFetchDaemon

app = FastAPI()

fetch_daemon = YoutubeFetchDaemon()

@asynccontextmanager
async def lifespan():
    # start daemon on app startup
    video_fetch_task = asyncio.create_task(fetch_daemon.start_fetching())
    yield

    # when app is stopped, kill daemon
    fetch_daemon.stop_fetching()
    await video_fetch_task

@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Up and running"}

@app.get("/videos", response_model=PaginatedResponse)
async def get_videos(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=50)):
    return await get_paginated_videos(page, page_size)

# TODO: run the fetch daemon on startup
