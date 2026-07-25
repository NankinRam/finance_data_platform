from pathlib import Path
from src.repository import conn_postgresql, bronze_rep
import pandas as pd

# Загрузка данных в базу
def load_data(df_bronze: pd.DataFrame):
    df = df_bronze.copy()
    df = df.drop("Номер", axis=1)

    bronze_rep.insert_bronze_sber_oper(df)

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