#!/usr/bin/env python

"""Flipkart.com Scraper"""

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

# Flipkart url
FLIPKART_URL = "https://www.flipkart.com/laptops/pr?sid=6bo,b5g&marketplace=FLIPKART"

def scrape_data(url):
    """Data Scraping Function"""
    # start the driver
    driver = webdriver.Chrome()
    driver.get(url)

    products = []
    prices = []
    ratings = []

    # get page content
    content = driver.page_source

    soup = BeautifulSoup(content, features="html.parser")

    for a in soup.findAll("a", href=True, attrs={"class": "_1fQZEK"}):
        name = a.find('div', attrs={'class': '_4rR01T'}).text
        price = a.find('div', attrs={'class': '_30jeq3 _1_WHN1'}).text
        rating = a.find('div', attrs={'class': '_3LWZlK'})

        products.append(name)
        prices.append(price)
        ratings.append(rating.text if rating else "None")

    driver.quit()
    return products, prices, ratings

def create_dataframe(products, prices, ratings):
    """Create a dataframe from the lists"""
    return pd.DataFrame({'Product Name': products, 'Price': prices, 'Rating': ratings})

def save_to_csv(dataframe, filename):
    """Save the df to a csv file"""
    return dataframe.to_csv(filename, index=False, encoding='utf-8')

if __name__ == "__main__":
    scraped_products, scraped_prices, scraped_ratings = scrape_data(url=FLIPKART_URL)
    data_frame = create_dataframe(scraped_products, scraped_prices, scraped_ratings)
    save_to_csv(data_frame, 'products.csv')
