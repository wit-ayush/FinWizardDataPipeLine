from config.constants import TICKER_TOKENS
from utils.data_handler import update_index_data

def main():
    for index_name, token in TICKER_TOKENS.items():
        update_index_data(index_name, token)

if __name__ == "__main__":
    main()
