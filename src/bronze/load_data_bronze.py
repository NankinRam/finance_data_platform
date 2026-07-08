from pathlib import Path

from src.bronze import transfer_bronze
from src.connect_sql import conn_postgresql
import pandas as pd

if __name__ == "__main__":

    df = transfer_bronze.refact_exel_to_csv()
    df = df.drop("Номер", axis=1)

    conn = conn_postgresql.connect()
    cursor = conn.cursor()

    print(df.info())

    query = """    
        INSERT INTO bronze.sber_oper (oper_date, type_oper, category, amount, cur, amount_rub, description, status, card)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

    for row in df.itertuples(index=False, name=None):
        cursor.execute(query, row)

    conn.commit()

    cursor.close()
    conn.close()