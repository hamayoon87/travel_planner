import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_amadeus_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": os.getenv("AMADEUS_API_KEY"),
        "client_secret": os.getenv("AMADEUS_API_SECRET")
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    res = requests.post(url, data=payload, headers=headers)
    return res.json()["access_token"]

def get_db_headers():
    return {
        "DB-Client-Id": os.getenv("DB_CLIENT_ID"),
        "DB-Api-Key": os.getenv("DB_API_KEY"),
        "Accept": "application/json"
    }

def get_station_eva_number(station_name):
    headers = get_db_headers()
    url = f"https://apis.deutschebahn.com/station-data/v1/locations?input={station_name}"
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    data = res.json()

    for item in data:
        if "evaNumbers" in item and item["evaNumbers"]:
            return item["evaNumbers"][0]
    
    raise ValueError(f"No EVA number found for station: {station_name}")


def get_hotel_location(city_code):
    token = get_amadeus_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-city?cityCode={city_code}"
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    data = res.json()
    
    if data["data"]:
        return data["data"][0]["geoCode"]  # Use geoCode for hotel search
    else:
        raise Exception(f"No hotels found for city code: {city_code}")
