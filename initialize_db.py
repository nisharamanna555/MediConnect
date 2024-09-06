import os
import psycopg2
from dotenv import load_dotenv

def run_sql_file(filename, conn):
    with open(filename, 'r') as file:
        sql = file.read()
        with conn.cursor() as cursor:
            cursor.execute(sql)
        conn.commit()

# check if database is empty
def database_is_empty(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        table_count = cursor.fetchone()[0]
        return table_count == 0
    


# Function to drop all tables in the database
def drop_all_tables(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            DO $$ 
            DECLARE
                r RECORD;
            BEGIN
                -- Dynamically generate and execute the DROP command for each table, excluding system tables
                FOR r IN (SELECT tablename 
                          FROM pg_tables 
                          WHERE schemaname = 'public' 
                          AND tablename NOT IN ('spatial_ref_sys')) LOOP
                    EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
                END LOOP;
            END $$;
        """)
        conn.commit()
        print("All existing tables (except system tables) have been dropped.")





def main():
    load_dotenv()
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        raise Exception("DATABASE_URL environment variable not set")
    
    # connect to the PostgreSQL database
    conn = psycopg2.connect(db_url)




    drop_all_tables(conn)


    run_sql_file('db_creation/create.sql', conn)
    run_sql_file('db_creation/insert.sql', conn)


    # run the SQL files to create tables and insert data if database is empty
    # if database_is_empty(conn):
        # Run the SQL files to create tables and insert data
        # run_sql_file('db_creation/create.sql', conn)
        # run_sql_file('db_creation/insert.sql', conn)
        # print("Database was successfully initialized.")
    # else:
        # print("Database is not empty, skipping table creation and data insertion.")

    # close the connection
    conn.close()

if __name__ == "__main__":
    main()
