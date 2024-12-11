from fastapi import APIRouter
from .endpoints import flights

router = APIRouter()
router.include_router(flights.router, prefix="/flights", tags=["Flights"])
