# Инсерт в bronze.sber_oper
import pandas as pd
from psycopg2._psycopg import cursor

from src.repository import conn_postgresql


def insert_bronze_sber_oper(df: pd.DataFrame, conn):

    cursor = conn.cursor()

    query = """
            INSERT INTO bronze.sber_oper (oper_date, type_oper, category, amount, cur, amount_rub, description, status, \
                                          card)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

    for row in df.itertuples(index=False, name=None):
        cursor.execute(query, row)

    conn.commit()
    cursor.close()