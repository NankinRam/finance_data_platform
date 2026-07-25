from pathlib import Path
import shutil
import pandas as pd

from src.bronze import bronze_data
from src.utils import data_parser


BASE_DIR = Path(__file__).resolve().parent.parent.parent

RAW_ORIGIN_FILE = BASE_DIR / "data" / "raw" / "original"
ARCHIVE_ORIGIN_FILE = BASE_DIR / "data" / "archive" / "original"


def preparing_raw_file():

    files = RAW_ORIGIN_FILE.rglob("*.xlsx")

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

        new_name_file = f"{year}_{month}_{day}.xlsx"

        # Создаем новые директории в archive
        new_archive_direct = ARCHIVE_ORIGIN_FILE / f"{year}" / f"{month}" / f"{day}"
        new_archive_direct.mkdir(parents=True, exist_ok=True)
        # Копируем файл в архив
        shutil.copy2(file, new_archive_direct)

        # Удаляем файл
        file.unlink()

    df_income = bronze_data.rename_attribute_df(df_income, 'Номер счета/карты зачисления',
                                                'Номер счета')
    df_outcome = bronze_data.rename_attribute_df(df_outcome, 'Номер счета/карты списания',
                                                 'Номер счета')

    df_all = bronze_data.concat_two_df(df_income, df_outcome)
    df_all = bronze_data.sort_df(df_all, 'Дата')

    new_raw_direct = RAW_ORIGIN_FILE.parent / f"{year}" / f"{month}" / f"{day}"

    new_raw_direct.mkdir(
        parents=True,
        exist_ok=True
    )

    df_all.to_excel(
        new_raw_direct / f"{year}_{month}_{day}.xlsx",
        index=False
    )

    return df_all
















