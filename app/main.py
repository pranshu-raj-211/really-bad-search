from fastapi import FastAPI, Query
from models.video_model import PaginatedResponse
from db.db_utils import get_paginated_videos

app = FastAPI()

@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Up and running"}

@app.get("/videos", response_model=PaginatedResponse)
async def get_videos(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=50)):
    return await get_paginated_videos(page, page_size)

# TODO: run the fetch daemon on startup