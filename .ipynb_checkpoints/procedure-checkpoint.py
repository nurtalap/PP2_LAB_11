import psycopg2
from config import load_config
from connect import get_connect

# Create the stored procedure
def create_procedure(config):
    conn = get_connect(config)
    cur = conn.cursor()
    cur.execute("""
        CREATE OR REPLACE PROCEDURE insert_or_update_user(p_name VARCHAR, p_phone VARCHAR)
        LANGUAGE plpgsql
        AS $$
        BEGIN
            IF EXISTS (SELECT 1 FROM PhoneBook WHERE name = p_name) THEN
                UPDATE PhoneBook
                SET phone = p_phone
                WHERE name = p_name;
            ELSE
                INSERT INTO PhoneBook (name, phone)
                VALUES (p_name, p_phone);
            END IF;
        END;
        $$;
    """)
    conn.commit()
    print("Stored procedure 'insert_or_update_user' created successfully.")
    cur.close()
    conn.close()

# Call the stored procedure
def insert_or_update_user(name, phone, config):
    conn = get_connect(config)
    cur = conn.cursor()
    cur.execute("CALL insert_or_update_user(%s, %s);", (name, phone))
    conn.commit()
    print(f"User '{name}' inserted or updated successfully.")
    cur.close()
    conn.close()

def main():
    config = load_config()
    create_procedure(config)
    
    while True:
        name = input("Enter user name (or type 'exit' to quit): ")
        if name.lower() == 'exit':
            break
        phone = input("Enter user phone: ")
        insert_or_update_user(name, phone, config)

if __name__ == '__main__':
    main()
