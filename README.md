# Really bad search

Building a very basic abstraction on top of youtube's list API.

Planned as a multi container app, running this requires filling in the environment variables in the .env file (multiple youtube api keys separated by just a `,`).

After this step execute docker compose -up in this dir in the terminal of your choice, while ensuring docker daemon is running.

Side note- SQLite or even a csv/flat file would be the best database for an app with these requirements, but I'm not save some hassle because I'm currently bedridden(temporary thing, need a couple weeks).
