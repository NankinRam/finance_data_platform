import pandas as pd
import psycopg2.extensions as pc
from psycopg2._psycopg import cursor

from src.repository import type_query


def insert_db(df: pd.DataFrame, conn: pc.connection, type_insert: str):
    df_new = df.copy()
    cursor = conn.cursor()

    query = type_query.get_query()[type_insert]

    for row in df_new.itertuples(index=False, name=None):
        cursor.execute(query, row)

    cursor.close()

# Получение df CATEGORY из БД
def select_category_db(conn: pc.connection):
    query = """
            SELECT categ_id, categ_name \
            FROM silver.CATEGORY \
            """
    return pd.read_sql(query, conn)


# Получение df TYPE_OPER из БД
def select_type_oper_db(conn: pc.connection):
    query = """
            SELECT type_id, type_name \
            FROM silver.TYPE_OPER \
            """
    return pd.read_sql(query, conn)