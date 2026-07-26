import pandas as pd
import psycopg2.extensions as pc
from src.repository import conn_postgresql, type_query
from dotenv import load_dotenv
import os

load_dotenv()

# Загрузка df в таблицу TRN
def insert_db(df: pd.DataFrame, conn: pc.connection, type_insert: str):
    df_new = df.copy()
    cursor = conn.cursor()

    query = type_query.get_query()[type_insert]

    for row in df_new.itertuples(index=False, name=None):
        cursor.execute(query, row)

    conn.commit()
    cursor.close()


# Получение df CATEGORY из БД
def select_category_db(conn: pc.connection):
    query = """
            SELECT categ_name \
            FROM silver.CATEGORY \
            """
    return pd.read_sql(query, conn)


# Получение df TYPE_OPER из БД
def select_type_oper_db(conn: pc.connection):
    query = """
            SELECT type_name \
            FROM silver.TYPE_OPER \
            """
    return pd.read_sql(query, conn)
