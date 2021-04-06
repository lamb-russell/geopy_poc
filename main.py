import csv
import os
from geopy.geocoders import MapBox
from geopy.extra.rate_limiter import RateLimiter

ENV_VAR="MAPBOX_API_TOKEN"


def get_token():
    """
    get api token from enviornment
    :return: api token
    """
    api_key = os.environ.get(ENV_VAR)
    if not api_key:
        raise PermissionError(f"API key missing in environment variable {ENV_VAR}")
        return None
    return api_key

def process_rows(file_path, start_row=None, end_row=None, one_result=True):
    """
    process rows in file
    :param file_path: path to CSV file
    :param start_row: starting row number (1 based)
    :param end_row: ending row number (1 based)
    :param one_result: if True, return a single result per address.  if False, return a list of locations.
    :return: list of tuples with results.  first entry is input, second entry is output.
    """
    api_token = get_token()
    geolocator = MapBox(api_token)

    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0.2)

    rowcount = 0
    results = [] # store results as list
    with open(file_path, newline="") as f: # open csv file
        reader = csv.reader(f)
        for row in reader:
            rowcount = rowcount + 1
            old_address = row[0] #assumes one address per line
            if start_row and rowcount < start_row: #skip rows preceding start parameter
                continue
            if end_row and rowcount > end_row: # stop when we exceed end param
                break
            new_address = geocode(old_address, exactly_one=one_result)
            results.append((old_address,new_address))

    return results


if __name__=="__main__":
    result = process_rows("5k_raw_address.csv", 10, 15)
    print(result)



