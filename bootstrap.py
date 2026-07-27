from pathlib import Path
from src.logger import log

BASE_DIR = Path(__file__).resolve().parent

# Пока добавлено чтобы было, после надо пивести в нормальный вид
def init():
    file = create_file()

    if file == 1:
        return False
    else:
        return True

def create_file():
    file_archive = BASE_DIR / "data" / "archive" / "origin"
    file_raw = BASE_DIR / "data" / "raw" / "origin"

    if file_archive.exists() and file_raw.exists():
        return 0
    else:
        file_archive.mkdir(True, True)
        file_raw.mkdir(True, True)

        log.info("✔ Файлы для работы были созданы")
        log.info("✔ Ожидаем входные данные в директории /data/raw/origin/")

        return 1
