from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import pandas as pd
import asyncio

# Import modules
from models.GreenSearchRequest import FlightSearchRequest
from controllers.airlines.local.GreenAfrica.main import scrape_green_flights_data
from controllers.airlines.local.AirPeace.main import scrape_air_peace_flights_data
from controllers.airlines.local.ArikAir.main import scrape_arik_air_flights_data
from controllers.airlines.local.IbomAir.main import scrape_ibom_air_flights_data

app = FastAPI()


@app.get("/scrape")
async def scrape(departing: str, arrival: str, departure_date: str, return_date: Optional[str] = None, trip_type: str = "one-way"):
    # Create the search request
    request = FlightSearchRequest(
        departing=departing,
        arrival=arrival,
        departure_date=departure_date,
        return_date=return_date,
        trip_type=trip_type
    )

    try:
        # Call scraper functions concurrently
        results = await asyncio.gather(
            scrape_green_flights_data(request),
            scrape_air_peace_flights_data(request),
            scrape_arik_air_flights_data(request),
            scrape_ibom_air_flights_data(request),
            return_exceptions=True 
        )

        # Combine results and handle exceptions
        flights = []
        for result in results:
            if isinstance(result, Exception):
                # Log or handle the exception (if needed)
                continue
            flights.extend(result.get("flights", []))

        # Convert to DataFrame
        df = pd.DataFrame(flights)

        # Return JSON response
        return JSONResponse(content=df.to_dict(orient="records"))

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@app.get("/")

def read_root():
    return {"message": "FastAPI is running!"}


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
 