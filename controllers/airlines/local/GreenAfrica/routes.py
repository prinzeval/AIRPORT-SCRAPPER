from fastapi import APIRouter
from models import FlightSearchRequest
from scraping import get_green_africa_url, scrape_flights_data

router = APIRouter()

@router.post("/search-flights/")
def search_flights(request: FlightSearchRequest):
    link = get_green_africa_url(request.departing, request.arrival, request.departure_date, request.return_date, request.trip_type)
    print(f"Constructed URL: {link}")

    # Scrape flight data
    flights = scrape_flights_data(link, request.departure_date, request.return_date, request.trip_type)

    return {"flights": flights}
