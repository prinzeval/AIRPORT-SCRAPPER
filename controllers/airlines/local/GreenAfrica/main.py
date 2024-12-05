from models.SearchRequest import FlightSearchRequest
from controllers.airlines.local.GreenAfrica.scraping import scrape as scrape_flights_data
from helper.date import reformat_date

def get_green_africa_url(Departing, Arrival, Departure_date, Return_date=None, Trip_Type="one-way"):
    Departure_date = reformat_date(Departure_date, "greenafrica")
    Return_date = reformat_date(Return_date, "greenafrica") if Return_date else None

    if Trip_Type == "round-trip":
        TEMPLATE = "https://greenafrica.com/booking/select?origin={}&destination={}&departure={}&return={}&round=1&adt=1&chd=0&inf=0"
        url = TEMPLATE.format(Departing, Arrival, Departure_date, Return_date)
    else:
        TEMPLATE = "https://greenafrica.com/booking/select?origin={}&destination={}&departure={}&adt=1&chd=0&inf=0"
        url = TEMPLATE.format(Departing, Arrival, Departure_date)
    return url

async def scrape_green_flights_data(request: FlightSearchRequest):
    link = get_green_africa_url(request.departing, request.arrival, request.departure_date, request.return_date, request.trip_type)
    print(f"Constructed URL: {link}")

    # Scrape flight data
    flights = await scrape_flights_data(link, request.departure_date, request.return_date, request.trip_type)

    return {"flights": flights}
