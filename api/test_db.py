import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

#database_url = os.getenv("DATABASE_URL")
database_url = os.getenv("DATABASE_URL", "sqlite:///test.db")
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

# Ensure that the test.db file is created and located correctly.
engine = create_engine(database_url)

try:
    connection = engine.connect()
    print("Successfully connected to the database.")
    connection.close()
except Exception as e:
    print(f"An error occurred: {e}")