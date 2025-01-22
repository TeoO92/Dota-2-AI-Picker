import os
from dotenv import load_dotenv

def config():
    load_dotenv() # Loads environmental variables from .env file (or Render)
    DATABASE_URL = os.getenv('DATABASE_URL')
    if DATABASE_URL is None:
        raise Exception("DATABASE_URL environment variable is not set.")
    return {"dsn": DATABASE_URL}

if __name__ == '__main__':
    config()