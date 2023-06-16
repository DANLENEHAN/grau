import configparser
import os
import time

from grau.db.functions import get_db_engine

# Get the database URL from the environment variable
db_url = os.environ.get("DATABASE_URL")

# Load the alembic.ini file
config = configparser.ConfigParser()
config.read("alembic.ini")

# Update the sqlalchemy.url value
config.set(
    "alembic",
    "sqlalchemy.url",
    db_url or "postgresql+psycopg2://dan:testing123@localhost/train",
)

# Save the changes back to the alembic.ini file
with open("alembic.ini", "w") as config_file:
    config.write(config_file)

# Wait for the database to be up
retry_count = 0
wait_time = 3
engine = get_db_engine()
db_up = False
while retry_count < 2:
    try:
        engine.connect()
        db_up = True
    except Exception as e:
        print(f"DB not up yet, waiting for {wait_time} seconds")
        time.sleep(3)
    finally:
        retry_count += 1
engine.dispose()

if not db_up:
    print("DB not up, exiting")
    exit(1)
else:
    print("DB is up, continuing")
