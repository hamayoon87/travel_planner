from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from travel import get_flights, summarize_flights
from fastapi.openapi.utils import get_openapi
import json

app = FastAPI(
    title="Travel Planner Tool",
    version="1.0.0",
    description="API to search flights, hotels, and train schedules for travel planning"
)

# Define your schema
class TravelQuery(BaseModel):
    name: Optional[str] = None
    origin: str
    destination: str
    start_date: str
    end_date: str
    travelers: int = 1

# Register your route
@app.post("/plan-trip", summary="Plan full trip", response_description="Combined travel info")
def plan_trip(query: TravelQuery):
    flights_raw = get_flights(query.origin, query.destination, query.start_date)
    flights_summary = summarize_flights(flights_raw)
    
    # Create a readable summary string
    summary_lines = []
    for f in flights_summary:
        summary_lines.append(
            f"{f['departure_airport']} at {f['departure_time']} → {f['arrival_airport']} at {f['arrival_time']}, Duration {f['duration']}, Price {f['price']} EUR"
        )
    summary_text = "\n".join(summary_lines)
    
    message = f"Trip for {query.name or 'guest'} from {query.origin} to {query.destination} planned.\nHere are the flight options:\n{summary_text}"
    
    return {
        "flights": flights_summary,
        "message": message
    }


# Custom OpenAPI generator – to be called AFTER routes are registered
def custom_openapi():
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["openapi"] = "3.0.3"
    openapi_schema["servers"] = [
        {"url": "http://localhost:8000", "description": "Local server"}
    ]

    # Save spec to file
    with open("openapi_watsonx.json", "w") as f:
        json.dump(openapi_schema, f, indent=2)

    return openapi_schema

# Assign AFTER route definitions
app.openapi = custom_openapi
