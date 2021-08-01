import logging
import sys

import config
import save_handler
import secret

# this script is called by crwonjob or similar util
# uses api and config scripts

# change this to your api key


def download_option_data(api_key: str):
    logger = logging.getLogger("main")
    symbol_list = config.symbol_list()["list"]

    n_symbols = len(symbol_list)

    for i, symbol in enumerate(symbol_list):
        # progress info
        logger.info(f"{i + 1}/{n_symbols} ({(i + 1) / n_symbols * 100:.2f}%) downloading data for {symbol}...")

        save_handler.save_contract_list(api_key, symbol)
        save_handler.save_all_option_chains(api_key, symbol)


# setup for the logging module
# all loggers should be children of logger "main"
def logging_setup():
    logger = logging.getLogger("main")

    stdout_handler = logging.StreamHandler(sys.stdout)
    logfile_handler = logging.FileHandler(config.logging_location())

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    stdout_handler.setFormatter(formatter)
    logfile_handler.setFormatter(formatter)

    logger.addHandler(stdout_handler)
    logger.addHandler(logfile_handler)

    logger.setLevel(logging.DEBUG)


def main():

    logging_setup()
    logger = logging.getLogger("main")

    logger.warning("Starting downloads")

    if save_handler.was_market_open(secret.TRADIER_API_KEY):
        download_option_data(secret.TRADIER_API_KEY)
    else:
        logger.warning("market wasn't open")


if __name__ == "__main__":
    main()