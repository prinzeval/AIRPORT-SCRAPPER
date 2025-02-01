from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def initialize_driver():
    # Set Chrome options for headless browsing
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = "/opt/chrome/chrome"
    chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
    chrome_options.add_argument("--no-sandbox")  # Disables the sandbox security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Prevents issues with Docker's limited memory space
    chrome_options.add_argument("--disable-gpu")  # Disables GPU acceleration (not needed in headless mode)
    chrome_options.add_argument("--disable-dev-tools")  # Disables DevTools (useful for running in Docker)
    chrome_options.add_argument("--no-zygote")  # Runs without the zygote process (needed in some environments)
    chrome_options.add_argument("--single-process")  # Avoids issues with multiple processes in headless mode
    chrome_options.add_argument("window-size=2560x1440")  # Sets a default window size (can help with responsive sites)
    chrome_options.add_argument("--user-data-dir=/tmp/chrome-user-data")  # Temporary user data directory for Chrome
    chrome_options.add_argument("--remote-debugging-port=9222")  # Allows remote debugging (useful for troubleshooting)

    # Set up the ChromeDriver service
    service = Service(executable_path="/opt/chromedriver")

    # Initialize the WebDriver with the Chrome service and options
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver



# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager

# def initialize_driver():
#     # Set Chrome options for headless browsing
#     chrome_options = Options()
#     chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
#     chrome_options.add_argument("--no-sandbox")  # Disables the sandbox security model
#     chrome_options.add_argument("--disable-dev-shm-usage")  # Prevents issues with Docker's limited memory space
#     chrome_options.add_argument("--disable-gpu")  # Disables GPU acceleration (not needed in headless mode)
#     chrome_options.add_argument("--disable-dev-tools")  # Disables DevTools (useful for running in Docker)
#     chrome_options.add_argument("--no-zygote")  # Runs without the zygote process (needed in some environments)
#     # chrome_options.add_argument("--single-process")  # Avoids issues with multiple processes in headless mode
#     chrome_options.add_argument("window-size=2560x1440")  # Sets a default window size (can help with responsive sites)
#     chrome_options.add_argument("--user-data-dir=/tmp/chrome-user-data")  # Temporary user data directory for Chrome
#     chrome_options.add_argument("--remote-debugging-port=9222")  # Allows remote debugging (useful for troubleshooting)

#     # Set up ChromeDriver using ChromeDriverManager
#     service = Service(ChromeDriverManager().install())

#     # Initialize the WebDriver with the Chrome service and options
#     driver = webdriver.Chrome(service=service, options=chrome_options)

#     return driver
