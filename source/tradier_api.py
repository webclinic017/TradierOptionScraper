import requests
import json

from datetime import datetime

import config

# properly convert the responses to json (dict) objects
def get_to_json(endpoint, api_key, params):
    api_type = config.api_type()

    response = requests.get(f"https://{api_type}.tradier.com{endpoint}",
        params=params,
        headers={"Authorization": f"Bearer {api_key}", "Accept": "application/json"}
    )

    # 2xx success status code
    if 200 <= response.status_code < 300:
        try:
            response_json = json.loads(response.text)
            return response_json
        except Exception as e:
            print(f"error parsing json response!\n{e}")
            return

    # error
    else: 
        print(response.status_code)
        print(response.text)
        return


# exactly matches the option relatet endpoints of the tradier api

def get_option_chains(api_key: str, symbol: str, expiration: datetime, greeks: bool = True):

    params = {'symbol': symbol, 'expiration': str(expiration).split()[0], 'greeks': str(greeks).lower()}
    return get_to_json("/v1/markets/options/chains", api_key, params)


def get_option_strikes(api_key: str, symbol: str, expiration: datetime):

    params = {'symbol': symbol, 'expiration': str(expiration).split()[0]}
    return get_to_json("/v1/markets/options/strikes", api_key, params)


def get_options_expirations(api_key: str, symbol: str, include_all_roots: bool = True, strikes: bool = True):

    params = {'symbol': symbol, 'includeAllRoots': str(include_all_roots).lower(), 'strikes': str(strikes).lower()}
    return get_to_json("/v1/markets/options/expirations", api_key, params)


def lookup_options_symbols(api_key: str, underlying: str):

    params = {'underlying': underlying}
    return get_to_json("/v1/markets/options/lookup", api_key, params)


# calender api to know when to download option data
# defaults to current month
def get_calender(api_key: str, month: int = None, year: int = None):

    month = datetime.today().month if month is None else month
    year = datetime.today().year if year is None else year

    params = {"month": month, "year": year}
    return get_to_json("/v1/markets/calendar", api_key, params)