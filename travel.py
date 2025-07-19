import requests
from utils import get_amadeus_token, get_station_eva_number, get_db_headers, get_hotel_location

def get_flights(origin, destination, date):
    token = get_amadeus_token()
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "originLocationCode": origin.upper(),       # Ensure 3-letter IATA code
        "destinationLocationCode": destination.upper(),
        "departureDate": date,
        "adults": 1
    }
    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    res = requests.get(url, headers=headers, params=params)
    return res.json()

def get_hotels(city_code, checkin_date, checkout_date):
    token = get_amadeus_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Lookup geo coordinates
    geo = get_hotel_location(city_code)
    
    url = "https://test.api.amadeus.com/v3/shopping/hotel-offers"
    params = {
        "latitude": geo["latitude"],
        "longitude": geo["longitude"],
        "checkInDate": checkin_date,
        "checkOutDate": checkout_date,
        "adults": 1
    }
    res = requests.get(url, headers=headers, params=params)
    res.raise_for_status()
    return res.json()


def get_train_schedule(from_city, to_city, date):
    try:
        from_eva = get_station_eva_number("Berlin Hbf")
        to_eva = get_station_eva_number("Munich Hbf")
    except Exception as e:
        return {"error": str(e)}

    date_str = date.replace("-", "")  # Format: YYYYMMDD
    hour = "00"  # Could be customized
    headers = get_db_headers()
    station_name = "Berlin Hbf"  # instead of BER
    url = "https://api.deutschebahn.com/stada/v2/stations?searchstring={station_name}"

    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return {"error": f"Timetable fetch failed: {res.text}"}

    return res.text
