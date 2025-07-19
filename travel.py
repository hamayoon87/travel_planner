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


def summarize_flights(flights_json):
    summary = []
    for flight in flights_json.get("data", []):
        itinerary = flight["itineraries"][0]
        segments = itinerary["segments"]
        dep = segments[0]["departure"]
        arr = segments[-1]["arrival"]
        price = flight["price"]["total"]
        summary.append({
            "departure_airport": dep["iataCode"],
            "departure_time": dep["at"],
            "arrival_airport": arr["iataCode"],
            "arrival_time": arr["at"],
            "duration": itinerary["duration"],
            "price": price,
        })
    return summary