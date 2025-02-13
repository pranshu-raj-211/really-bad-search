# Really bad search

Building a very basic abstraction on top of youtube's list API.

Continuously pulls the latest videos for specified search terms.

Features
- Continuously fetches latest YouTube videos in the background.
- API key rotation to handle quota limits.
- Paginated API responses.
- MongoDB storage with proper indexing.
- Async api implementation for better performance and concurrency.

## Design Decisions
Background Fetching
- Uses FastAPI's lifespan context manager for managing the background task lifecycle
- Implements a generator-based API key rotation system for handling quota limits
- Configurable fetch interval (default: 10 seconds)

## Database
- Currently using synchronous PyMongo for simplicity
- Indexes on video_id (unique) and published_datetime (for sorting)
- Upsert operations to prevent duplicates

## API Endpoints
GET /
Health check endpoint.

GET /videos
Get paginated video results.

#### Parameters:

page: Page number (default: 1)
page_size: Items per page (default: 10, max: 50)


## How to run

1. Clone the repo, cd into the repo

2. Create and populate the env file, based on example env params (api keys separated by a comma only)

3. Use docker compose as

`docker-compose up -d`







Planned as a multi container app, running this requires filling in the environment variables in the .env file (multiple youtube api keys separated by just a `,`).

After this step execute docker compose -up in this dir in the terminal of your choice, while ensuring docker daemon is running.

Side note- SQLite or even a csv/flat file would be the best database for an app with these requirements, but I'm not save some hassle because I'm currently bedridden(temporary thing, need a couple weeks).
