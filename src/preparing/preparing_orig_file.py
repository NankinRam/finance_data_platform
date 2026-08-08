from pathlib import Path
import shutil
import pandas as pd

from src.bronze import bronze_data
from src.service import minio_service
from src.service.minio_service import MinioService
from src.utils import data_parser


BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_FILE = BASE_DIR / "data"

def preparing_raw_file():

    minio = MinioService()

    files = DATA_FILE.rglob("*.xlsx")

    df_income = pd.DataFrame
    df_outcome = pd.DataFrame

    day = ""
    month = ""
    year = ""

    for file in files:
        name_file = file.name

        split_file = name_file.replace(" ", "_").split("_")

        if split_file[0] == 'income':
            df_income = pd.read_excel(file)
        if split_file[0] == 'outcome':
            df_outcome = pd.read_excel(file)

        day = split_file[1]
        month = data_parser.months()[split_file[2].replace(".", "")]
        year = split_file[3].replace(",", "")

        # Удаляем файл
        # file.unlink()

    df_income = bronze_data.rename_attribute_df(df_income, 'Номер счета/карты зачисления',
                                                'Номер счета')
    df_outcome = bronze_data.rename_attribute_df(df_outcome, 'Номер счета/карты списания',
                                                 'Номер счета')

    df_all = bronze_data.concat_two_df(df_income, df_outcome)
    df_all = bronze_data.sort_df(df_all, 'Дата')

    name_df_in_minio = f"origin/{year}_{month}_{day}.csv"

    minio.load_df(name_df_in_minio, df_all)

    return name_df_in_minio













