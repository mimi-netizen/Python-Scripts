import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import time
from datetime import datetime
import re

class BooksFirstScraper:
    def __init__(self):
        self.base_url = "https://booksfirst.africa"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.data = []

    def clean_price(self, price_str):
        if not price_str:
            return None
        try:
            # Extract price value (assuming USD format)
            return float(re.sub(r'[^\d.]', '', price_str))
        except (ValueError, TypeError):
            return None

    def clean_text(self, text):
        if text:
            return ' '.join(text.strip().split())
        return None

    def scrape_books(self, category):
        try:
            url = f"{self.base_url}/{category}"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            books = soup.find_all('div', class_='product-item')
            
            for book in books:
                try:
                    # Extract book details
                    name = self.clean_text(book.find('h3', class_='product-title').text)
                    price_elem = book.find('span', class_='price')
                    price = self.clean_price(price_elem.text) if price_elem else None
                    
                    # Get author if available
                    author_elem = book.find('span', class_='author')
                    author = self.clean_text(author_elem.text) if author_elem else None

                    # Check if book is on sale
                    sale_price = None
                    if book.find('span', class_='sale-price'):
                        sale_price = self.clean_price(book.find('span', class_='sale-price').text)

                    self.data.append({
                        'name': name,
                        'author': author,
                        'price': price,
                        'sale_price': sale_price,
                        'category': category
                    })

                except AttributeError as e:
                    logging.error(f"Error parsing book data: {str(e)}")
                    continue

            return len(books) > 0

        except requests.RequestException as e:
            logging.error(f"Error fetching category {category}: {str(e)}")
            return False

    def save_to_csv(self, filename=None):
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'booksfirst_data_{timestamp}.csv'
        
        try:
            df = pd.DataFrame(self.data)
            df.to_csv(filename, index=False, encoding='utf-8')
            logging.info(f"Data successfully saved to {filename}")
            return filename
        except Exception as e:
            logging.error(f"Error saving data to CSV: {str(e)}")
            return None

def main():
    # Set up logging
    logging.basicConfig(
        filename='booksfirst_scraper.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    scraper = BooksFirstScraper()
    
    print("Welcome to the Books First Africa Scraper!")
    print("\nAvailable categories:")
    categories = [
        'african-interest', 'autobiography', 'business', 
        'childrens-books', 'fiction', 'self-help-inspirational'
    ]
    
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category}")
    
    category_choice = int(input("\nEnter category number to scrape (1-6): ").strip())
    if 1 <= category_choice <= len(categories):
        selected_category = categories[category_choice - 1]
        
        print(f"\nScraping books from {selected_category}...")
        if scraper.scrape_books(selected_category):
            filename = scraper.save_to_csv()
            if filename:
                print(f"\nData successfully saved to {filename}")
                print(f"Total books scraped: {len(scraper.data)}")
            else:
                print("Error saving data to CSV file")
        else:
            print("No books found in this category")
    else:
        print("Invalid category selection")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScraping interrupted by user")
        logging.info("Scraping interrupted by user")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        logging.error(f"Unexpected error: {str(e)}")