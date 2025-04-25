import psycopg2
from connect import get_connect
from config import load_config

def create_function(config):
    conn = get_connect(config)
    cur = conn.cursor()
    cur.execute("""
        CREATE OR REPLACE PROCEDURE search_users(p_pattern VARCHAR, INOUT ref refcursor)
        LANGUAGE plpgsql
        AS $$
        BEGIN
            OPEN ref FOR
                SELECT *
                FROM PhoneBook
                WHERE name ILIKE '%' || p_pattern || '%'
                OR phone ILIKE '%' || p_pattern || '%';
        END;
        $$;
    """)
    conn.commit()
    print("Stored procedure 'search_users' created successfully.")
    cur.close()
    conn.close()


def call_search_users(pattern, config):
    conn = get_connect(config)
    cur = conn.cursor()
    
    try:
        cur.execute("BEGIN;")
        cur.execute("CALL search_users(%s, 'search_result');", (pattern,))
        cur.execute("FETCH ALL FROM search_result;")
        rows = cur.fetchall()
        
        if rows:
            for row in rows:
                print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")
        else:
            print("No matching users found.")
        
        cur.execute("CLOSE search_result;")
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def main():
    config = load_config()
    pattern = input("Enter pattern to search (part of name or phone): ")
    create_function(config)
    call_search_users(pattern, config)

if __name__ == '__main__':
    main()
