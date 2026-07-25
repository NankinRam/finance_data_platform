from pathlib import Path
from src.repository import conn_postgresql, bronze_rep
import pandas as pd

def load_data(df_bronze: pd.DataFrame):
    df = df_bronze.copy()
    df = df.drop("Номер", axis=1)

    conn = conn_postgresql.connect()
    cursor = conn.cursor()

    query = bronze_rep.insert_bronze_sber_oper()

    for row in df.itertuples(index=False, name=None):
        cursor.execute(query, row)

    conn.commit()

    cursor.close()
    conn.close()