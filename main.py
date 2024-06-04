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
import owala

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
            'handlers': ['file'],
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
logger.info('starting script')

def create_database():
    conn = sqlite3.connect(os.getenv('DATABASE_NAME'))
    c = conn.cursor()
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS bottles(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            release_date TEXT,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    '''
    c.execute(create_table_query)
    conn.commit()
    conn.close()

def save_to_database(name, release_date):
    conn = sqlite3.connect(os.getenv('DATABASE_NAME'))
    c = conn.cursor()
    c.execute("INSERT INTO bottles (name, release_date) VALUES (?, ?)", (name, release_date))
    conn.commit()
    conn.close()
    logger.info(f'Saved to database: {name}, {release_date}, {button_text}')


def scrape_website(driver, url):
    # print(f"Scraping website {url}")
    logger.info(f'scraping {url}')
    owala.scrape(driver, url, logger)    


def main():
    create_database()

    # Set up Selenium WebDriver
    options = Options()
    # options.headless = True  # Run in headless mode (without opening a browser window)
    options.add_argument('--headless')
    options.binary_location = os.getenv('CHROME_BROWSER_PATH')  # Path to Chrome binary on macOS
    service = Service(executable_path='./chromedriver', log_path='NUL')  # Replace with your WebDriver's path
    driver = webdriver.Chrome(service=service, options=options)

    if os.getenv('TRACK_OWALA') == 'True':
        url = os.getenv('OWALA_URL')
        if not url:
            raise ValueError("OWALA_URL environment variable is not set.")
        scrape_website(driver, url)
    driver.quit()

    
if __name__ == '__main__':
    main()