import bootstrap
from src.bronze import bronze_data
from src.logger import log
from src.preparing import preparing_orig_file
from src.repository import conn_postgresql
from src.silver import silver_data

def main():

    if bootstrap.init():
        conn = conn_postgresql.connect()

        df_origin = preparing_orig_file.preparing_raw_file()
        df_bronze = bronze_data.load_data(df_origin, conn)
        df_silver = silver_data.processing_data_silver(df_bronze, conn)

        conn.commit()
        conn.close()
        log.info("Close connect PostgreSQL DB:finance")


if __name__ == '__main__':
    main()