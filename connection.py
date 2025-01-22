import psycopg2
from config import config

def connect():
    conn = None
    try:
        params = config() # Obtain Render PostgreSQL connection string
        DATABASE_URL = params['dsn']
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(DATABASE_URL)  # Connect to the db using the string
        return conn
    except (Exception, psycopg2.DatabaseError) as error: # Error exeption managment
        print(error)

if __name__ == '__main__':
    connect()