from pathlib import Path, PurePosixPath
from pandas.core.interchange.dataframe_protocol import DataFrame
import io
from src.repository import conn_postgresql, finance_rep
import pandas as pd

from src.service.minio_service import MinioService

def processing_data(path_minio: str, conn):
    minio = MinioService()
    response = minio.unload_df(path_minio)

    df = pd.DataFrame()

    try:
        df = pd.read_csv(io.BytesIO(response.read()))
    finally:
        response.close()
        response.release_conn()

    df = delete_attribute(df, "Номер")

    load_data(df, conn)
    raw_path = load_minio(df, minio, path_minio)

    return raw_path


# Загрузка в MinIO
def load_minio(df_bronze: DataFrame, minio: MinioService, path_minio: str):

    source_path = PurePosixPath(path_minio)
    new_path = source_path.parent.parent / "raw" / source_path.name

    df = df_bronze.copy()

    minio.load_df(f"{new_path}", df)

    return new_path


# Загрузка данных в базу
def load_data(df_bronze: DataFrame , conn):

    df = df_bronze.copy()
    finance_rep.insert_db(df, conn, 'INSERT_SBER_OPER')

    return df


# Функция объединения двух DataFrame-ов
def concat_two_df(df1: pd.DataFrame, df2: pd.DataFrame):
    df_concat = pd.concat([df1, df2], ignore_index=True)
    return df_concat


# Функция переименования столбца
def rename_attribute_df(df: pd.DataFrame, old_name_attr: str, new_name_attr : str):
    df_rename = df.copy()
    df_rename = df_rename.rename(columns={f"{old_name_attr}" : f"{new_name_attr}"})
    return df_rename


# Функция сортировка DF по значению
def sort_df(df: pd.DataFrame, values: str):
    df_sort = df.copy()
    df_sort = df_sort.sort_values(f"{values}", ascending=True)
    return df_sort


# Функция для удаления столбца
def delete_attribute(df: pd.DataFrame, attr: str):
    df_delete = df.copy()
    df_delete = df_delete.drop(f"{attr}", axis=1)
    return df_delete