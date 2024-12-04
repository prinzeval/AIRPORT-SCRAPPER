from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from models import FlightSearchRequest
from scraping import get_url, scrape_flights_data
from typing import Optional

router = APIRouter()

@router.get("/scrape")
def scrape(departing: str = Query(..., description="Departure location"), 
           arrival: str = Query(..., description="Arrival location"), 
           departure_date: str = Query(..., description="Departure date (e.g., dd.mm.yyyy)"), 
           return_date: Optional[str] = Query(None, description="Return date (e.g., dd.mm.yyyy)")):
    link = get_url(departing, arrival, departure_date, return_date, "round-trip" if return_date else "one-way")
    flights = scrape_flights_data(link)
    return JSONResponse(content=flights)
