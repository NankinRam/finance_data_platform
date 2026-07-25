from src.bronze import bronze_data
from src.preparing import preparing_orig_file
import pandas as pd

def main():
    df = preparing_orig_file.preparing_raw_file()
    bronze_data.load_data(df_bronze=df)

if __name__ == '__main__':
    main()