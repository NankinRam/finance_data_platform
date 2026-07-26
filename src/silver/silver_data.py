# Точка входа для обработки silver
import pandas as pd

from src.repository import silver_rep


def processing_data_silver(df: pd.DataFrame, conn):
    df_silver = df.copy()

    create_df_category(df_silver, conn)
    create_df_type_oper(df_silver, conn)

    return df_silver


# Создание df CATEGORY
def create_df_category(df: pd.DataFrame, conn):

    new_df_cat = df.copy()
    new_df_cat = (
        new_df_cat[['Категория']]
        .drop_duplicates(ignore_index=True)
    )

    new_df_cat = new_df_cat.rename(columns={"Категория": "categ_name"})

    old_df_cat = silver_rep.select_category_db(conn)
    if old_df_cat.empty:
        silver_rep.insert_db(new_df_cat, conn, "INSERT_CATEGORY")
    else:
        df_cat_unik = new_df_cat[~new_df_cat['categ_name'].isin(old_df_cat["categ_name"])]
        silver_rep.insert_db(df_cat_unik, conn, "INSERT_CATEGORY")


# Создание df TYPE_OPER
def create_df_type_oper(df: pd.DataFrame, conn):

    new_df_oper = df.copy()
    new_df_oper = (
        new_df_oper[['Тип операции']]
        .drop_duplicates(ignore_index=False)
    )

    old_df_oper = silver_rep.select_type_oper_db(conn)
    if old_df_oper.empty:
        silver_rep.insert_db(new_df_oper, conn, 'INSERT_TYPE_OPER')
    else:
        df_oper_unik = new_df_oper[~new_df_oper['Тип операции'].isin(old_df_oper['type_name'])]
        silver_rep.insert_db(df_oper_unik, conn, 'INSERT_TYPE_OPER')

