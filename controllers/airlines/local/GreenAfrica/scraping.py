from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from typing import Optional, List, Dict

def get_green_africa_url(Departing, Arrival, Departure_date, Return_date=None, Trip_Type="one-way"):
    if Trip_Type == "round-trip":
        TEMPLATE = "https://greenafrica.com/booking/select?origin={}&destination={}&departure={}&return={}&round=1&adt=1&chd=0&inf=0"
        url = TEMPLATE.format(Departing, Arrival, Departure_date, Return_date)
    else:
        TEMPLATE = "https://greenafrica.com/booking/select?origin={}&destination={}&departure={}&adt=1&chd=0&inf=0"
        url = TEMPLATE.format(Departing, Arrival, Departure_date)
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

def scrape_flights_data(link: str, departure_date: str, return_date: Optional[str], trip_type: str) -> List[Dict[str, str]]:
    driver = initialize_driver()
    
    driver.get(link)
    sleep(20)
    flight_rows = driver.find_elements(By.XPATH, '//div[@class="chakra-accordion css-1po3p4o"]')
    
    flights = []

    for WebElement in flight_rows:
        elementHTML = WebElement.get_attribute('outerHTML')
        elementsoup = BeautifulSoup(elementHTML, 'html.parser')

        # FLIGHT INFO BOX 1
        flight_box1 = elementsoup.find('div', {"class": "align-center w-full lg:w-max grow"})
        depart_time = flight_box1.find_all("h3", {"class": "text-h4 lg:text-[30px] font-700 text-[#17181A] text-center"})[0].text.strip()
        depart_loc = flight_box1.find_all("p", {"class": "text-sm lg:text-p mt-4 text-dark300 text-center"})[0].text.strip()
        duration = flight_box1.find("p", {"class": "text-12 lg:text-sm text-dark300 border-t-1 border-solid border-dark100 text-center pt-14 font-500"}).text.strip()
        arrive_time = flight_box1.find_all("h3", {"class": "text-h4 lg:text-[30px] font-700 text-[#17181A] text-center"})[1].text.strip()
        arrive_loc = flight_box1.find_all("p", {"class": "text-sm lg:text-p mt-4 text-dark300 text-center"})[1].text.strip()

        # FLIGHT INFO BOX 2
        flight_no = elementsoup.select_one('.align-center .lg\\:p-9:nth-of-type(1) p:nth-of-type(2)').text.strip()
        total_stop = elementsoup.select_one('.align-center .lg\\:p-9:nth-of-type(2) p:nth-of-type(2)').text.strip()

        # Initialize prices
        business_price = None
        economy_price = None
        executive_economy_price = None

        packages = elementsoup.find_all('div', class_='box-shadow')

        for package in packages:
            title = package.find('h4').get_text(strip=True)
            price = package.find('span', class_='text-[30px]').get_text(strip=True)
            
            if title.lower() == "gsaver":
                economy_price = price
            elif title.lower() == "gclassic":
                business_price = price
            elif title.lower() == "gflex":
                executive_economy_price = price

        flight_data = {
            'FLIGHT DEPART': depart_loc,
            'FLIGHT ARRIVAL': arrive_loc,
            'DEPART TIME': depart_time,
            'ARRIVAL TIME': arrive_time,
            'DEPART DATE': departure_date,
            'ARRIVAL DATE': return_date if trip_type == "round-trip" else departure_date,
            'FLIGHT DURATION': duration,
            'TOTAL STOP': total_stop,
            'FLIGHT NO': flight_no,
            'BUSINESS PRICE': business_price,
            'ECONOMY PRICE': economy_price,
            'EXECUTIVE ECONOMY PRICE': executive_economy_price
        }
        flights.append(flight_data)
    
    driver.quit()
    
    return flights