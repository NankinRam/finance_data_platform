from src.bronze import bronze_data
from src.logger import log
from src.preparing import preparing_orig_file
from src.repository import conn_postgresql
from src.silver import silver_data

def main():
    conn = conn_postgresql.connect()

    name_origin_minio = preparing_orig_file.preparing_raw_file()
    print(f"name_origin_minio -> {name_origin_minio}")

    name_raw_minio = bronze_data.processing_data(name_origin_minio, conn)
    print(f"name_raw_minio -> {name_raw_minio}")

    silver_data.processing_data_silver(name_raw_minio, conn)

    conn.commit()
    conn.close()
    log.info("Close connect PostgreSQL DB:finance")


if __name__ == '__main__':
    main()