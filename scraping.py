from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv

# Setup Chrome options to run headlessly
chrome_options = Options()
chrome_options.add_argument("--headless")

import os

# Set the path to the ChromeDriver executable
CHROMEDRIVER_PATH = '/path/to/chromedriver'  # Change this to the location of your chromedriver

# Set the system property
os.environ["webdriver.chrome.driver"] = CHROMEDRIVER_PATH

driver = webdriver.Chrome(options=chrome_options)

BASE_URL = 'http://books.toscrape.com/catalogue/'
data = []

# Number of pages to scrape. Adjust this value as needed.
num_pages = 5

for page in range(1, num_pages + 1):
    page_url = BASE_URL + f"page-{page}.html"
    driver.get(page_url)

    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    books = soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')

    for book in books:
        # Basic Info
        title = book.h3.a.attrs['title']
        price = float(book.find('p', class_='price_color').text[1:])
        rating = book.find('p', class_='star-rating')['class'][1]

        # Navigate to the book details page using Selenium
        book_link = BASE_URL + book.h3.a.attrs['href']
        driver.get(book_link)

        # Parse the book details page with BeautifulSoup
        book_soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Genre
        genre = book_soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip()

        # Availability
        availability = book_soup.find('p', class_='availability').text.strip()

        # Description
        description = book_soup.find('meta', attrs={'name': 'description'})['content'].strip()

        data.append([title, price, rating, genre, availability, description])
        print(title, price, rating, genre, availability, description)

        # Navigate back to the listing page
        driver.back()

    print(f"Scraped page {page}")

driver.quit()

# Saving data to CSV
filename = 'books_data.csv'
with open(filename, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Price', 'Rating', 'Genre', 'Availability', 'Description'])
    writer.writerows(data)
    print(data)

print(f'Data saved to {filename}')
