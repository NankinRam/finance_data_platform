# Точка входа для обработки silver
import io
import locale
from pathlib import PurePosixPath

import pandas as pd
import locale as lc
from src.repository import finance_rep
from src.service.minio_service import MinioService

lc.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


def processing_data_silver(path_minio: str, conn):
    minio = MinioService()
    response = minio.unload_df(f"{path_minio}")

    try:
        df_silver = pd.read_csv(io.BytesIO(response.read()))
    finally:
        response.close()
        response.release_conn()

    create_df_category(df_silver, conn)
    create_df_type_oper(df_silver, conn)

    df_cat = finance_rep.select_category_db(conn)
    df_type_oper = finance_rep.select_type_oper_db(conn)

    mapping_cat = df_cat.set_index('categ_name')['categ_id']
    mapping_type_oper = df_type_oper.set_index('type_name')['type_id']

    df_silver['Категория'] = df_silver['Категория'].map(mapping_cat)
    df_silver['Тип операции'] = df_silver['Тип операции'].map(mapping_type_oper)

    df_silver['Дата'] = pd.to_datetime(df_silver['Дата'], format='%d %b. %Y, %H:%M')

    finance_rep.insert_db(df_silver, conn, 'INSERT_TRN')


# Создание df CATEGORY
def create_df_category(df: pd.DataFrame, conn):

    new_df_cat = df.copy()
    new_df_cat = (
        new_df_cat[['Категория']]
        .drop_duplicates(ignore_index=True)
    )

    new_df_cat = new_df_cat.rename(columns={"Категория": "categ_name"})

    old_df_cat = finance_rep.select_category_db(conn)
    if old_df_cat.empty:
        finance_rep.insert_db(new_df_cat, conn, "INSERT_CATEGORY")
    else:
        df_cat_unik = new_df_cat[~new_df_cat['categ_name'].isin(old_df_cat["categ_name"])]
        if not df_cat_unik.empty:
            finance_rep.insert_db(df_cat_unik, conn, "INSERT_CATEGORY")


# Создание df TYPE_OPER
def create_df_type_oper(df: pd.DataFrame, conn):

    new_df_oper = df.copy()
    new_df_oper = (
        new_df_oper[['Тип операции']]
        .drop_duplicates(ignore_index=False)
    )

    old_df_oper = finance_rep.select_type_oper_db(conn)
    if old_df_oper.empty:
        finance_rep.insert_db(new_df_oper, conn, 'INSERT_TYPE_OPER')
    else:
        df_oper_unik = new_df_oper[~new_df_oper['Тип операции'].isin(old_df_oper['type_name'])]
        if not df_oper_unik.empty:
            finance_rep.insert_db(df_oper_unik, conn, 'INSERT_TYPE_OPER')

