from src.bronze import bronze_data
from src.preparing import preparing_orig_file
import pandas as pd

from src.repository import conn_postgresql, silver_rep
from src.silver import silver_data


def main():

    conn = conn_postgresql.connect()

    df_origin = preparing_orig_file.preparing_raw_file()
    df_bronze = bronze_data.load_data(df_origin, conn)
    df_silver = silver_data.processing_data_silver(df_bronze, conn)

    conn.close()


if __name__ == '__main__':
    main()