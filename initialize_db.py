import os
import psycopg2
from dotenv import load_dotenv

def run_sql_file(filename, conn):
    with open(filename, 'r') as file:
        sql = file.read()
        with conn.cursor() as cursor:
            cursor.execute(sql)
        conn.commit()

def main():
    load_dotenv()
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        raise Exception("DATABASE_URL environment variable not set")
    
    # connect to the PostgreSQL database
    conn = psycopg2.connect(db_url)

    # run the SQL files to create tables and insert data
    run_sql_file('db_creation/create.sql', conn)
    run_sql_file('db_creation/insert.sql', conn)

    # close the connection
    conn.close()

if __name__ == "__main__":
    main()
