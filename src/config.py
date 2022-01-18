import os
import json
import logging

# load and read config
logger = logging.getLogger(__name__)

CONFIG_FILE_NAME = "../config.json"


# (re)loads the config from disk
def load_config() -> dict:
    config_path = os.path.join(os.getcwd(), CONFIG_FILE_NAME)

    try:
        with open(config_path, "r") as f:
            config_json = json.load(f)

    except Exception as e:
        logger.critical(f"Can't load config. Aborting!\n{e}")
        exit(1)

    return config_json


def get_config() -> dict:
    return CONFIG_DICT


def get_secret() -> str:
    try:
        with open(get_config()["secret"], "r") as f:
            secrets = f.read()
            if secrets.isascii():
                return secrets
            else:
                logger.critical("Secret should only include printable characters! Aborting!")
                exit(1)
    except IOError as e:
        logger.critical(f"Api secret file not found! Aborting!\n{e}")
        exit(1)


def get_loglevel() -> int:
    try:
        return getattr(logging, get_config()["logging_level"])
    except AttributeError as e:
        logger.warning(f"Debug level specified in config not found. Defaulting to WARNING level.\n{e}")
        return logging.WARNING


def get_symbols() -> list:
    try:
        with open(get_config()["symbol_list_file"], "r") as f:
            return json.load(f)["symbols"]
    except IOError as e:
        logger.critical(f"Could not find symbols list file {get_config()['symbol_list_file']}\n{e}")
    except json.JSONDecodeError as e:
        logger.critical(f"Could not decode symbol list file\n{e}")


CONFIG_DICT = load_config()
