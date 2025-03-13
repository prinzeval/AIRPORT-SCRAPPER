from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import asyncio
import pandas as pd
from mangum import Mangum
import json

from models.GreenSearchRequest import FlightSearchRequest
from controllers.airlines.local.GreenAfrica.main import scrape_green_flights_data
from controllers.airlines.local.AirPeace.main import scrape_air_peace_flights_data
from controllers.airlines.local.ArikAir.main import scrape_arik_air_flights_data
from controllers.airlines.local.IbomAir.main import scrape_ibom_air_flights_data

app = FastAPI()

@app.get("/scrape")
async def scrape(departing: str, arrival: str, departure_date: str, return_date: Optional[str] = None, trip_type: str = "one-way"):
    request = FlightSearchRequest(
        departing=departing,
        arrival=arrival,
        departure_date=departure_date,
        return_date=return_date,
        trip_type=trip_type
    )

    try:
        # Use asyncio.gather to run scraping concurrently, with added logging
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
                print(f"Error scraping: {str(result)}")  # Log error for debugging
                continue
            if 'flights' in result:
                flights.extend(result['flights'])
            else:
                print(f"No flight data returned from {result}")  # Log if no data is returned

        if not flights:
            raise HTTPException(status_code=404, detail="No flights found for the given parameters.")

        df = pd.DataFrame(flights)

        # Return the result as JSON
        return JSONResponse(content=df.to_dict(orient="records"))

    except Exception as e:
        # Log the exception for debugging
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "Airline Scanner is live!"}


handler = Mangum(app)  # Ensures compatibility with Lambda
