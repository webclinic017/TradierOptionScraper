import datetime
import json
import logging
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
import data_util
from apis import tradier


# this script is called by cronjob or similar util
# uses api and config scripts

# setup for the logging module
# all loggers should be children of logger "main"
def logging_setup(stdout_logging_level):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    stdout_handler = logging.StreamHandler(sys.stdout)
    logfile_handler = logging.FileHandler(config.get_config("logging_location"))

    stdout_handler.setLevel(stdout_logging_level)
    logfile_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    stdout_handler.setFormatter(formatter)
    logfile_handler.setFormatter(formatter)

    logger.addHandler(stdout_handler)
    logger.addHandler(logfile_handler)


def main():
    logging_setup(config.get_loglevel())
    logger = logging.getLogger("main")

    logger.warning("Starting downloads...")

    tradier_api = tradier.TradierAPI()
    tradier_api.download_all(data_util.Symbol("AAPL", None, None), data_util.TimeInterval.day)


if __name__ == "__main__":
    main()
