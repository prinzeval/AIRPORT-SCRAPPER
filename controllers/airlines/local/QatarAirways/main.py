def generate_qatar_airways_url(departure: str, destination: str, date: str) -> str:
    base_url = "https://www.qatarairways.com/app/booking/flight-selection"
    params = {
        "widget": "QR",
        "searchType": "F",
        "addTaxToFare": "Y",
        "minPurTime": "0",
        "selLang": "en",
        "tripType": "O",
        "fromStation": departure,
        "toStation": destination,
        "departing": date,
        "bookingClass": "E",
        "adults": "1",
        "children": "0",
        "infants": "0",
        "ofw": "0",
        "teenager": "0",
        "flexibleDate": "off"
    }
    query_string = "&".join([f"{key}={value}" for key, value in params.items()])
    return f"{base_url}?{query_string}"

# Example usage
departure = "IST"
destination = "LOS"
date = "2024-12-09"
url = generate_qatar_airways_url(departure, destination, date)
print(url)
