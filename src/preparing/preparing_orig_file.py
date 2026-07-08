from pathlib import Path
import shutil

MONTHS = {
    "янв": 1,
    "фев": 2,
    "мар": 3,
    "апр": 4,
    "май": 5,
    "июн": 6,
    "июл": 7,
    "авг": 8,
    "сен": 9,
    "окт": 10,
    "ноя": 11,
    "дек": 12,
}

BASE_DIR = Path(__file__).resolve().parent.parent.parent

RAW_ORIGIN_FILE = BASE_DIR / "data" / "raw" / "original"
ARCHIVE_ORIGIN_FILE = BASE_DIR / "data" / "archive" / "original"


def preparing_raw_file():

    files = RAW_ORIGIN_FILE.rglob("*.xlsx")

    new_path = ""

    for file in files:
        name_file = file.name

        split_file = name_file.split("_")

        day = split_file[1]
        month = MONTHS[split_file[2]]
        year = split_file[3]

        new_name_file = f"{year}_{month}_{day}.xlsx"

        # Создаем новые директории в archive
        new_archive_direct = ARCHIVE_ORIGIN_FILE / f"{year}" / f"{month}" / f"{day}"
        new_archive_direct.mkdir(parents=True, exist_ok=True)
        # Копируем файл в архив
        shutil.copy2(file, new_archive_direct)

        # Создаем новые директории в raw
        new_raw_direct = RAW_ORIGIN_FILE.parent / f"{year}" / f"{month}" / f"{day}"
        new_raw_direct.mkdir(parents=True, exist_ok=True)
        # Переносим файл в raw
        file = file.rename(new_name_file)
        shutil.move(file, new_raw_direct)

        new_path = new_raw_direct / new_name_file

    return new_path
