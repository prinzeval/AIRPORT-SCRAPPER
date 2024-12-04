from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def get_url(Departing: str, Arrival: str, Departure_date: str) -> str:
    TEMPLATES = "https://book-airpeace.crane.aero/ibe/availability?tripType=ONE_WAY&depPort={}&arrPort={}&departureDate={}%20%20%20%20%20%20%20%20&adult=1&child=0&infant=0&lang=en"
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

def scrape_flights_data(link: str):
    driver = initialize_driver()
    
    try:
        driver.get(link)
        sleep(2)
        
        flight_rows = driver.find_elements(By.XPATH, '//div[@class="row w-100 no-gutters"]')
        
        depart_time_list = []
        depart_loc_list = []
        depart_date_list = []
        flight_duration_list = []
        total_stop_list = []
        flight_no_list = []
        arrival_time_list = []
        arrival_loc_list = []
        arrival_date_list = []
        economy_price_list = []
        executive_economy_price_list = []
        business_price_list = []
        
        for WebElement in flight_rows:
            elementHTML = WebElement.get_attribute('outerHTML')
            elementsoup = BeautifulSoup(elementHTML, 'html.parser')
            
            flight_box1 = elementsoup.find('div', {"class": "info-block"})
            depart_time = flight_box1.find("span", {"class": "time"})
            depart_loc = flight_box1.find("span", {"class": "port"})
            depart_date = flight_box1.find("span", {"class": "date"})
            depart_time_list.append(depart_time.text if depart_time else "N/A")
            depart_loc_list.append(depart_loc.text if depart_loc else "N/A")
            depart_date_list.append(depart_date.text if depart_date else "N/A")
            sleep(2)

            flight_box2 = elementsoup.find('div', {"class": "info-row"})
            flight_duration = flight_box2.find("span", {"class": "flight-duration"})
            total_stop = flight_box2.find("span", {"class": "total-stop"})
            flight_no = flight_box2.find("span", {"class": "flight-no"})
            flight_duration_list.append(flight_duration.text if flight_duration else "N/A")
            total_stop_list.append(total_stop.text if total_stop else "N/A")
            flight_no_list.append(flight_no.text if flight_no else "N/A")
            sleep(2)

            flight_box3 = elementsoup.find('div', {"class": "info-block text-right"})
            arrival_time = flight_box3.find("span", {"class": "time"})
            arrival_loc = flight_box3.find("span", {"class": "port"})
            arrival_date = flight_box3.find("span", {"class": "date"})
            arrival_time_list.append(arrival_time.text if arrival_time else "N/A")
            arrival_loc_list.append(arrival_loc.text if arrival_loc else "N/A")
            arrival_date_list.append(arrival_date.text if arrival_date else "N/A")
            sleep(1)

            flight_box4 = elementsoup.find('div', {'class': "desktop-fare-block"})
            economy_price = flight_box4.find("span", {"class": "currency-best-offer"})
            if economy_price is not None:
                economy_price_list.append(economy_price.text.strip())
            else:
                economy_price = flight_box4.find("span", {"class": "currency"})
                economy_price_list.append(economy_price.text.strip() if economy_price else "no seat")
            sleep(1)

            executive_economy_price = flight_box4.find("span", {"class": "no-seat-text"})
            executive_economy_price_list.append(executive_economy_price.text.strip() if executive_economy_price else "no seat")

            business_price = flight_box4.find("span", {"class": "currency"})
            business_price_list.append(business_price.text.strip() if business_price else "no seat")
            sleep(2)

        Table = {
            'FLIGHT DEPART': depart_loc_list,
            'FLIGHT ARRIVAL': arrival_loc_list,
            'DEPART TIME': depart_time_list,
            'ARRIVAL TIME': arrival_time_list,
            'DEPART DATE': depart_date_list,
            'ARRIVAL DATE': arrival_date_list,
            'FLIGHT DURATION': flight_duration_list,
            'TOTAL STOP': total_stop_list,
            'FLIGHT NO': flight_no_list,
            'BUSINESS PRICE': business_price_list,
            'ECONOMY PRICE': economy_price_list,
            'EXECUTIVE ECONOMY PRICE': executive_economy_price_list
        }
        df = pd.DataFrame(Table)

        return df

    finally:
        driver.quit()
