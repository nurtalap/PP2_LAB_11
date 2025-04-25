import psycopg2
from connect import get_connect
from config import load_config

def create_delete_procedure(config):
    conn = get_connect(config)
    cur = conn.cursor()
    
    cur.execute("""
    CREATE OR REPLACE PROCEDURE delete_user(p_name VARCHAR, p_phone VARCHAR)
    LANGUAGE plpgsql
    AS $$
    BEGIN
        IF p_name IS NOT NULL AND p_phone IS NOT NULL THEN
            DELETE FROM PhoneBook
            WHERE name = p_name OR phone = p_phone;
            
        ELSIF p_name IS NOT NULL THEN
            DELETE FROM PhoneBook
            WHERE name = p_name;
            
        ELSIF p_phone IS NOT NULL THEN
            DELETE FROM PhoneBook
            WHERE phone = p_phone;
            
        ELSE
            RAISE NOTICE 'No name or phone provided. Nothing was deleted.';
        END IF;
    END;
    $$;
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    print("Procedure delete_user created successfully.")

def call_delete_user(name, phone, config):
    conn = get_connect(config)
    cur = conn.cursor()
    
    try:
        cur.execute("CALL delete_user(%s, %s);", (name, phone))
        conn.commit()
        print(f"Deleted user(s) with name = '{name}' or phone = '{phone}'.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while calling delete_user procedure: {error}")
    finally:
        cur.close()
        conn.close()

def main():
    config = load_config()
    
    name = input("Enter name to delete (or press Enter to skip): ").strip()
    phone = input("Enter phone to delete (or press Enter to skip): ").strip()
    
    # Приводим пустые строки к None
    if name == '':
        name = None
    if phone == '':
        phone = None
    
    call_delete_user(name, phone, config)

if __name__ == '__main__':
    main()