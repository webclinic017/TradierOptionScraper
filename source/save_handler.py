import json
import os

from datetime import datetime

import config
import tradier_api
import shutil

# saves to files at the given location
# format

# {save_location}/{symbol}/{current date YYYY-MM-DD}/contrats.json - list of all available contracts for this day
# {save_location}/{symbol}/{current date YYYY-MM-DD}/{experation date YYYY-MM-DD}.json - option chain for experation date

# determine if the market was open today
def was_market_open(api_key: str) -> bool:
    calender = tradier_api.get_calender(api_key)
    days = calender["calendar"]["days"]["day"]
    
    info_today = days[datetime.today().day - 1]
    return info_today["status"] == "open"

def mkdir(loaction):
    if not os.path.isdir(loaction):
        os.mkdir(loaction)

def get_save_loaction(symbol: str):
    save_location = config.save_location()
    mkdir(save_location)

    save_location = os.path.join(save_location, symbol)
    mkdir(save_location)

    save_location = os.path.join(save_location, str(datetime.today()).split()[0])
    mkdir(save_location)

    return save_location

def save_contract_list(api_key: str, symbol: str):
    save_location = get_save_loaction(symbol)
    contracts = tradier_api.lookup_options_symbols(api_key, symbol)

    with open(os.path.join(save_location, "contrats.json"), "w") as f:
        json.dump(contracts, f, indent=4)

def save_option_chain(api_key: str, symbol:str, expiration: datetime):
    save_location = get_save_loaction(symbol)
    option_chain = tradier_api.get_option_chains(api_key, symbol, expiration)
    filename = f"{str(expiration).split()[0]}.json"

    with open(os.path.join(save_location, filename), "w") as f:
        json.dump(option_chain, f, indent=4)

def save_all_option_chains(api_key: str, symbol: str):
    location = get_save_loaction(symbol)
    if os.path.isfile(f"{location}.zip"):
        return

    expirations = tradier_api.get_options_expirations(api_key, symbol, strikes=False)
    try:
        expirations = expirations["expirations"]["date"]
    except Exception as e:
        print(f"no options for symbol {symbol}\n{e}")
        return

    expirations = list(map(lambda x: datetime.fromisoformat(x), expirations))

    for exp in expirations:
        save_option_chain(api_key, symbol, exp)

    
    shutil.make_archive(location, "zip", location)
    shutil.rmtree(location)