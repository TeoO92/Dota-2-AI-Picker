import psycopg2
from config import config

def connect():
    conn = None
    try:
        params = config() # Ottieni la stringa di connessione
        DATABASE_URL = params['dsn']  # La stringa di connessione
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(DATABASE_URL)  # Connetti usando la stringa di connessione
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == '__main__':
    connect()