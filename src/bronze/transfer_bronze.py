from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).parent.parent.parent

def refact_exel_to_csv():
    path = (
            BASE_DIR /
            "data" /
            "raw" /
            "2026" /
            "06" /
            "30" /
            "outcome_30_июн_2026_00_00.xlsx"
    )

    df = pd.read_excel(path)

    return df