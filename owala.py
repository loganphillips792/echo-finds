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
from datetime import datetime
import pytz


def scrape(driver, url, logger):
    conn = sqlite3.connect(os.getenv('DATABASE_NAME'))
    c = conn.cursor()

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

        product_release_date_element = container.find_element(By.CLASS_NAME, 'product__release-date')
        product_release_date = product_release_date_element.text if product_release_date_element else 'N/A'

        # if the product is sold out, then the class is 'product__notify-btn'
        button_elements = container.find_elements(By.TAG_NAME, 'button')
        button_text = button_elements[0].text if button_elements else 'N/A'

        if 'Available Now' in product_release_date:
            logger.info(f'{product_name} is available now!')
            # if the product is available now, then the class is 'addcart-button'
            # button_element = container.find_element(By.CLASS_NAME, 'addcart-button')
            # button_text = button_element.text if button_element else 'N/A'
            c.execute("INSERT INTO bottles (name, release_date, status) VALUES (?, ?, ?)", (product_name, "", "Available Now"))
            conn.commit()

            logger.info(f'Available item Saved to database: {product_name}, "", {button_text}')
            
            continue
        elif 'Sold out' in button_text:
            logger.info(f'{product_name} is sold out!')
            c.execute("INSERT INTO bottles (name, release_date, status) VALUES (?, ?, ?)", (product_name, "", button_text))
            conn.commit()
        
            logger.info(f'Sold Out item Saved to database: {product_name}, {utc_time}, {button_text}')
            continue
        else:
            logger.info(f'product {product_name} will be released on {product_release_date}')

        # Extracting the date and time parts from the string
        parts = product_release_date.split()
        date_str = parts[1] # '7/9'
        time_str = parts[3] # '10:00'
        period = parts[4] # 'AM'
        timezone = parts[5] # 'MDT'

        # Construct the full date and time string
        date_time_str = f"2024-{date_str} at {time_str} {period}"

        # Define the format
        date_time_format = "%Y-%m/%d at %I:%M %p"

        # Create a datetime object
        local_tz = pytz.timezone("America/Denver")  # MDT corresponds to America/Denver

        local_time = datetime.strptime(date_time_str, date_time_format)

        # Localize the datetime object to the given timezone
        local_time = local_tz.localize(local_time)

        # Convert to UTC
        utc_time = local_time.astimezone(pytz.utc)

        logger.info(f"UTC time: {utc_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")

        c.execute("INSERT INTO bottles (name, release_date, status) VALUES (?, ?, ?)", (product_name, utc_time, button_text))
        conn.commit()
        
        logger.info(f'Saved to database: {product_name}, {utc_time}, {button_text}')
    conn.close()


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
        