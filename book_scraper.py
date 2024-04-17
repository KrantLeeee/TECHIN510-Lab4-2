import os
import requests
from bs4 import BeautifulSoup
from database import Database  # Make sure to have database.py in the same directory
from dotenv import load_dotenv

# Initialize the database connection
load_dotenv()
db_url = os.getenv("supabaseURL")
if db_url is None:
    raise ValueError("Database URL not found. Check your environment variables.")
db = Database(os.getenv("supabaseURL"))
db.create_table()
db.truncate_table()

# Base URL of the site
base_url = 'https://books.toscrape.com/catalogue'
page = 1

books = []

while True:
    URL = f'{base_url}/page-{page}.html'
    print(f'Scraping page {page}')
    response = requests.get(URL)

    # If the page doesn't exist, break the loop
    if response.status_code == 404:
        break
    
    soup = BeautifulSoup(response.text, 'html.parser')
    book_divs = soup.select('ol.row > li.col-xs-6.col-sm-4.col-md-3.col-lg-3')

    for book_div in book_divs:
        book = {}
        book['title'] = book_div.select_one('h3 a')['title']
        relative_url = book_div.select_one('h3 a')['href']
        book['book_id'] = relative_url.split('_')[1].split('/')[0]
        book_url = f'{base_url}/{relative_url}'
        book_response = requests.get(book_url)
        book_soup = BeautifulSoup(book_response.text, 'html.parser')
        # In case the description is None:
        description_elem = book_soup.select_one('#content_inner > article > p')
        book['description'] = description_elem.text.strip() if description_elem else ""

        book['price'] = book_div.select_one('p.price_color').text.replace('Â', '').strip()
        book['rating'] = book_div.select_one('p.star-rating')['class'][1]

        # Insert book data into the database
        books.append(book)
        db.insert_book(book)

    page += 1

db.close()  # Close the database connection when done
