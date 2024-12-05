from models.IbomSearchResult import FlightSearchRequest
from controllers.airlines.local.IbomAir.scraping import scrape as scrape_flights_data
from helper.date import reformat_date

def get_ibom_air_url(Departing, Arrival, Departure_date, Return_date=None, Trip_Type="one-way"):
    Departure_date = reformat_date(Departure_date, "ibomair")
    Return_date = reformat_date(Return_date, "ibomair") if Return_date else None
    
    if Trip_Type == "round-trip":
        TEMPLATE = "https://book-ibomair.crane.aero/ibe/availability?tripType=ROUND_TRIP&depPort={}&arrPort={}&departureDate={}&returnDate={}&adult=1&child=0&infant=0&lang=en"
        url = TEMPLATE.format(Departing, Arrival, Departure_date, Return_date)
    else:
        TEMPLATE = "https://book-ibomair.crane.aero/ibe/availability?tripType=ONE_WAY&depPort={}&arrPort={}&departureDate={}&adult=1&child=0&infant=0&lang=en"
        url = TEMPLATE.format(Departing, Arrival, Departure_date)
    return url

async def scrape_ibom_air_flights_data(request: FlightSearchRequest):
    link = get_ibom_air_url(request.departing, request.arrival, request.departure_date, request.return_date, request.trip_type)
    print(f"Constructed URL: {link}")

    # Scrape flight data
    flights = await scrape_flights_data(link, request.departure_date, request.return_date, request.trip_type)

    return {"flights": flights}
