from config import load_config
import psycopg2

def get_connect(config):
    conn = psycopg2.connect(**config)
    curr = conn.cursor()

    

config = load_config()
get_connect(config)