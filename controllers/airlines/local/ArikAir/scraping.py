from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from typing import Optional, List, Dict
from helper.driver import initialize_driver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

async def scrape(link: str, departure_date: str, return_date: Optional[str], trip_type: str) -> List[Dict[str, str]]:
    driver = initialize_driver()
    
    driver.get(link)
# Wait until the elements are available 
    WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.XPATH, '//div[@class="row w-100 no-gutters"]')) 
                                    ) 
    flight_rows = driver.find_elements(By.XPATH, '//div[@class="row w-100 no-gutters"]')
    
    flights = []

    for WebElement in flight_rows:
        elementHTML = WebElement.get_attribute('outerHTML')
        elementsoup = BeautifulSoup(elementHTML, 'html.parser')

        # FLIGHT INFO
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
        
        # Prices
        economy_price_best_offer = flight_box4.find("span", {"class": "currency-best-offer"})
        economy_price = economy_price_best_offer.text.strip() if economy_price_best_offer else ""
        economy_price_offer = flight_box4.find("span", {"class": "price-best-offer"})
        if economy_price_offer:
            economy_price += " " + economy_price_offer.text.strip()
        economy_price = economy_price.strip() if economy_price else "no seat"
        
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
            'EXECUTIVE ECONOMY PRICE': executive_economy_price,
            'AIRLINE':"ARIK AIR"
        }
        flights.append(flight_data)
    
    driver.quit()
    
    return flights
 