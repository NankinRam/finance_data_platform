import psycopg2

def connect():
    conn = psycopg2.connect(
        host="localhost",
        database="finance",
        user="finance",
        password="finance",
        port="5433"
    )

    return conn