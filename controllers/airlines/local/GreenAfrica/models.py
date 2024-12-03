from pydantic import BaseModel
from typing import Optional

class FlightSearchRequest(BaseModel):
    departing: str
    arrival: str
    departure_date: str
    return_date: Optional[str] = None
    trip_type: str  # "one-way" or "round-trip"
