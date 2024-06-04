import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
import os
from dotenv import load_dotenv
import logging
import logging.config

load_dotenv()

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'app.log',
            'formatter': 'standard',
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True
        },
        'my_module': {  # a specific logger for 'my_module'
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}

# Apply the logging configuration
logging.config.dictConfig(LOGGING_CONFIG)

# Create a logger
logger = logging.getLogger('my_module')

# use logger. If one is not specified, it will default to the root one
logging.info('starting script')

def create_database():
    conn = sqlite3.connect('water_bottles.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS bottles
                (name TEXT, release_date TEXT)''')
    conn.commit()
    conn.close()

def save_to_database(name, release_date):
    conn = sqlite3.connect('water_bottles.db')
    c = conn.cursor()
    c.execute("INSERT INTO bottles (name, release_date) VALUES (?, ?)", (name, release_date))
    conn.commit()
    conn.close()

def scrape_website(url):
    # print(f"Scraping website {url}")
    logging.info(f'scraping {url}')
    
    # Set up Selenium WebDriver
    options = Options()
    # options.headless = True  # Run in headless mode (without opening a browser window)
    options.add_argument('--headless')
    options.binary_location = os.getenv('CHROME_BROWSER_PATH')  # Path to Chrome binary on macOS
    service = Service(executable_path='./chromedriver', log_path='NUL')  # Replace with your WebDriver's path
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get(url)

    # Wait until the elements with class 'color-drop__blocks' are present. This is the grid of products
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'color-drop__blocks'))
    )
    
    # Wait for the elements to be present
    # wait = WebDriverWait(driver, 10)

    product_containers = driver.find_elements(By.CLASS_NAME,'product__text-container')

    product_details = []
    for container in product_containers:
        product_name_element = container.find_element(By.CLASS_NAME, 'product__name')
        product_name = product_name_element.text if product_name_element else 'N/A'
        logging.info(f'product name is {product_name}')


    # bottle_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.product__container')))  # Update this
    # release_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.some-class-for-date')))  # Update this

    # for bottle in bottle_elements:
    #         print("hi")
    #         print(bottle)

    # for bottle, release in zip(bottle_elements, release_elements):
    #     name = bottle.text.strip()
    #     release_date = release.text.strip()
    #     save_to_database(name, release_date)
    
    driver.close()
        

def main():
    create_database()

    if os.getenv('TRACK_OWALA') == 'True':
        url = os.getenv('OWALA_URL')
        if not url:
            raise ValueError("OWALA_URL environment variable is not set.")
        scrape_website(url)

    
if __name__ == '__main__':
    main()