from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import pandas as pd
import asyncio

from models.GreenSearchRequest import FlightSearchRequest
from controllers.airlines.local.GreenAfrica.main import scrape_green_flights_data
from controllers.airlines.local.AirPeace.main import scrape_air_peace_flights_data
from controllers.airlines.local.ArikAir.main import scrape_arik_air_flights_data
from controllers.airlines.local.IbomAir.main import scrape_ibom_air_flights_data

router = APIRouter()

@router.get("/scrape")
async def scrape(departing: str, arrival: str, departure_date: str, return_date: Optional[str] = None, trip_type: str = "one-way"):
    request = FlightSearchRequest(
        departing=departing,
        arrival=arrival,
        departure_date=departure_date,
        return_date=return_date,
        trip_type=trip_type
    )

    try:
        results = await asyncio.gather(
            scrape_green_flights_data(request),
            scrape_air_peace_flights_data(request),
            scrape_arik_air_flights_data(request),
            scrape_ibom_air_flights_data(request),
            return_exceptions=True 
        )

        flights = []
        for result in results:
            if isinstance(result, Exception):
                continue
            flights.extend(result.get("flights", []))

        df = pd.DataFrame(flights)
        return JSONResponse(content=df.to_dict(orient="records"))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
