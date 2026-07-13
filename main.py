from src.bronze import bronze_data
from src.preparing import preparing_orig_file

def main():
    path = preparing_orig_file.preparing_raw_file()
    bronze_data.load_data(path)

if __name__ == '__main__':
    main()