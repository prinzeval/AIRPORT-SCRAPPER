# Airport Scraper API

## Description
The **Airport Scraper API** is a Python-based web scraping tool designed to extract flight data from multiple airline websites. This tool provides structured information on flight schedules, prices, and other relevant details. It is optimized for scalability and performance, ensuring efficient data extraction for real-time applications.

## Features
- Scrapes flight data from multiple airline websites.
- Supports both one-way and round-trip searches.
- Returns results in JSON format for seamless integration.
- Built with modern Python libraries and tools for efficient scraping.
- Deployed using AWS Lambda and Docker for scalability.

## Technologies Used
- **FastAPI**: For building a robust and high-performance API.
- **BeautifulSoup**: For web scraping and data parsing.
- **Pandas**: For data cleaning and transformation.
- **AWS Lambda**: For cloud deployment and scalability.
- **Docker**: For containerizing the application for easy deployment.

## Requirements
- Python 3.10+
- AWS CLI configured with appropriate permissions.
- Docker installed (if deploying with Docker).

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/prinzeval/airport-scraper-api.git
    cd airport-scraper-api
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run locally:**
    ```bash
    uvicorn app:app --reload
    ```

4. **Access API Documentation:**
    Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for Swagger UI.

## Usage

### Endpoint: `/scrape`
- **Method:** GET
- **Parameters:**
  | Parameter       | Type   | Required | Description                              |
  |-----------------|--------|----------|------------------------------------------|
  | `departing`     | `str`  | Yes      | Departure airport code (e.g., LOS).      |
  | `arrival`       | `str`  | Yes      | Arrival airport code (e.g., ABV).        |
  | `departure_date`| `str`  | Yes      | Departure date in YYYY-MM-DD format.     |
  | `return_date`   | `str`  | No       | Return date in YYYY-MM-DD format (for round-trips). |
  | `trip_type`     | `str`  | No       | Trip type (one-way or round-trip). Default is one-way. |

### Example Request:
```bash
curl -X GET "http://127.0.0.1:8000/scrape?departing=LOS&arrival=ABV&departure_date=2024-12-15&trip_type=one-way"
```

### Example Response:
```json
[
     {
          "airline": "Green Africa",
          "flight_number": "G123",
          "departure_time": "10:00 AM",
          "arrival_time": "12:00 PM",
          "price": "25000 NGN"
     },
     {
          "airline": "Ibom Air",
          "flight_number": "IA456",
          "departure_time": "11:00 AM",
          "arrival_time": "1:00 PM",
          "price": "27000 NGN"
     }
]
```

## Deployment

### Deploying with AWS Lambda:
1. **Build and package the application:**
    ```bash
    docker build -t airport-scraper-api .
    docker run -v $(pwd):/app airport-scraper-api
    ```

2. **Deploy using AWS CLI:**
    ```bash
    aws lambda update-function-code --function-name airport-scraper-api --zip-file fileb://deployment-package.zip
    ```

### Deploying with Docker:
1. **Build Docker Image:**
    ```bash
    docker build -t airport-scraper-api .
    ```

2. **Run Docker Container:**
    ```bash
    docker run -p 8000:8000 airport-scraper-api
    ```

## Future Improvements
- Add caching mechanisms for faster repeated queries.
- Integrate more airlines for comprehensive data coverage.
- Optimize scraping scripts for dynamic websites using Selenium