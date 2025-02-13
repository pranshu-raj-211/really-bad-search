import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query, HTTPException
from models.video_model import PaginatedResponse
from db.db_utils import get_paginated_videos
from utils.log_config import logger
from services.pull_videos import YoutubeFetchDaemon

app = FastAPI()

fetch_daemon = YoutubeFetchDaemon()

@asynccontextmanager
async def lifespan():
    # start daemon on app startup
    video_fetch_task = asyncio.create_task(fetch_daemon.start_fetching())
    logger.info('Started pulling videos from youtube.')
    yield

    # when app is stopped, kill daemon
    fetch_daemon.stop_fetching()
    logger.info('Stopping pulling videos from api.')
    await video_fetch_task

@app.get("/")
async def root() -> dict[str, str]:
    logger.info('Server up')
    return {"message": "Up and running"}

@app.get("/videos", response_model=PaginatedResponse)
async def get_videos(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=50)):
    try:
        return await get_paginated_videos(page, page_size)
    except Exception as e:
        logger.error("Error occured while serving videos", extra={'exception':e})
        raise HTTPException(status_code=500, detail='Something went wrong while serving videos.')
