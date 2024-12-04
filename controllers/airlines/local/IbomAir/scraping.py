from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from typing import Optional, List, Dict

def get_url(Departing: str, Arrival: str, Departure_date: str, Return_date: Optional[str] = None, trip_type: str = "one-way") -> str:
    if trip_type.lower() == "round-trip":
        TEMPLATES = "https://book-ibomair.crane.aero/ibe/availability?tripType=ROUND_TRIP&depPort={}&arrPort={}&departureDate={}&returnDate={}&passengerQuantities%5B0%5D%5BpassengerType%5D=ADULT&passengerQuantities%5B0%5D%5BpassengerSubType%5D=&passengerQuantities%5B0%5D%5Bquantity%5D=1&passengerQuantities%5B1%5D%5BpassengerType%5D=CHILD&passengerQuantities%5B1%5D%5BpassengerSubType%5D=&passengerQuantities%5B1%5D%5Bquantity%5D=0&passengerQuantities%5B2%5D%5BpassengerType%5D=INFANT&passengerQuantities%5B2%5D%5BpassengerSubType%5D=&passengerQuantities%5B2%5D%5Bquantity%5D=0&currency=NGN&cabinClass=&lang=EN&nationality=&promoCode=&accountCode=&affiliateCode=&clickId=&withCalendar=&isMobileCalendar=&market=&isFFPoint="
        url = TEMPLATES.format(Departing, Arrival, Departure_date, Return_date)
    else:
        TEMPLATES = "https://book-ibomair.crane.aero/ibe/availability?tripType=ONE_WAY&depPort={}&arrPort={}&departureDate={}&returnDate=&passengerQuantities%5B0%5D%5BpassengerType%5D=ADULT&passengerQuantities%5B0%5D%5BpassengerSubType%5D=&passengerQuantities%5B0%5D%5Bquantity%5D=1&passengerQuantities%5B1%5D%5BpassengerType%5D=CHILD&passengerQuantities%5B1%5D%5BpassengerSubType%5D=&passengerQuantities%5B1%5D%5Bquantity%5D=0&passengerQuantities%5B2%5D%5BpassengerType%5D=INFANT&passengerQuantities%5B2%5D%5BpassengerSubType%5D=&passengerQuantities%5B2%5D%5Bquantity%5D=0&currency=NGN&cabinClass=&lang=EN&nationality=&promoCode=&accountCode=&affiliateCode=&clickId=&withCalendar=&isMobileCalendar=&market=&isFFPoint="
        url = TEMPLATES.format(Departing, Arrival, Departure_date)
    return url

def initialize_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scrape_flights_data(link: str) -> List[Dict[str, str]]:
    driver = initialize_driver()
    
    try:
        driver.get(link)
        sleep(2)
        
        flight_rows = driver.find_elements(By.XPATH, '//div[@class="row w-100 no-gutters"]')
        
        flights = []
        
        for WebElement in flight_rows:
            elementHTML = WebElement.get_attribute('outerHTML')
            elementsoup = BeautifulSoup(elementHTML, 'html.parser')
            
            flight_box1 = elementsoup.find('div', {"class": "info-block"})
            depart_time = flight_box1.find("span", {"class": "time"}).text.strip() if flight_box1.find("span", {"class": "time"}) else "N/A"
            depart_loc = flight_box1.find("span", {"class": "port"}).text.strip() if flight_box1.find("span", {"class": "port"}) else "N/A"
            depart_date = flight_box1.find("span", {"class": "date"}).text.strip() if flight_box1.find("span", {"class": "date"}) else "N/A"

            flight_box2 = elementsoup.find('div', {"class": "info-row"})
            flight_duration = flight_box2.find("span", {"class": "flight-duration"}).text.strip() if flight_box2.find("span", {"class": "flight-duration"}) else "N/A"
            total_stop = flight_box2.find("span", {"class": "total-stop"}).text.strip() if flight_box2.find("span", {"class": "total-stop"}) else "N/A"
            flight_no = flight_box2.find("span", {"class": "flight-no"}).text.strip() if flight_box2.find("span", {"class": "flight-no"}) else "N/A"

            flight_box3 = elementsoup.find('div', {"class": "info-block text-right"})
            arrival_time = flight_box3.find("span", {"class": "time"}).text.strip() if flight_box3.find("span", {"class": "time"}) else "N/A"
            arrival_loc = flight_box3.find("span", {"class": "port"}).text.strip() if flight_box3.find("span", {"class": "port"}) else "N/A"
            arrival_date = flight_box3.find("span", {"class": "date"}).text.strip() if flight_box3.find("span", {"class": "date"}) else "N/A"

            flight_box4 = elementsoup.find('div', {'class': "desktop-fare-block"})
            
            # Economy price
            economy_price_best_offer = flight_box4.find("span", {"class": "currency-best-offer"})
            economy_price = economy_price_best_offer.text.strip() if economy_price_best_offer else ""
            economy_price_offer = flight_box4.find("span", {"class": "price-best-offer"})
            if economy_price_offer:
                economy_price += " " + economy_price_offer.text.strip()
            economy_price = economy_price.strip() if economy_price else "no seat"
            
            # Business price
            business_price_best_offer = flight_box4.find("span", {"class": "currency"})
            business_price = business_price_best_offer.text.strip() if business_price_best_offer else ""
            business_price_offer = flight_box4.find("span", {"class": "price"})
            if business_price_offer:
                business_price += " " + business_price_offer.text.strip()
            business_price = business_price.strip() if business_price else "no seat"
            
            executive_economy_price = flight_box4.find("span", {"class": "no-seat-text"})
            executive_economy_price = executive_economy_price.text.strip() if executive_economy_price else "no seat"

            flight_data = {
                'FLIGHT DEPART': depart_loc,
                'FLIGHT ARRIVAL': arrival_loc,
                'DEPART TIME': depart_time,
                'ARRIVAL TIME': arrival_time,
                'DEPART DATE': depart_date,
                'ARRIVAL DATE': arrival_date,
                'FLIGHT DURATION': flight_duration,
                'TOTAL STOP': total_stop,
                'FLIGHT NO': flight_no,
                'BUSINESS PRICE': business_price,
                'ECONOMY PRICE': economy_price,
                'EXECUTIVE ECONOMY PRICE': executive_economy_price
            }

            flights.append(flight_data)
        
        return flights

    finally:
        driver.quit()
