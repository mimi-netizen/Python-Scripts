import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import time
from datetime import datetime
import re
from urllib.parse import urljoin, quote_plus

class ZLibraryScraper:
    def __init__(self):
        self.base_url = "https://z-lib.fm"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.books_data = []
        
        # Set up logging
        logging.basicConfig(
            filename='zlibrary_scraper.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def clean_text(self, text):
        if text:
            return ' '.join(text.strip().split())
        return None

    def clean_size(self, size_str):
        if not size_str:
            return None
        try:
            size = re.search(r'([\d.]+)\s*(MB|KB)', size_str)
            if size:
                value = float(size.group(1))
                unit = size.group(2)
                return f"{value} {unit}"
        except:
            pass
        return size_str

    def search_books(self, query, page=1, max_results=100):
        try:
            search_url = f"{self.base_url}/search"
            params = {
                'q': quote_plus(query),
                'page': page
            }
            
            response = self.session.get(
                search_url,
                params=params,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            books = soup.find_all('div', class_='book-info')  # Adjust class based on actual HTML
            
            for book in books:
                if len(self.books_data) >= max_results:
                    return False

                try:
                    # Extract book details
                    title_elem = book.find('h3', class_='title')
                    author_elem = book.find('div', class_='authors')
                    year_elem = book.find('div', class_='year')
                    format_elem = book.find('div', class_='format')
                    size_elem = book.find('div', class_='size')
                    language_elem = book.find('div', class_='language')
                    
                    book_data = {
                        'title': self.clean_text(title_elem.text) if title_elem else None,
                        'authors': self.clean_text(author_elem.text) if author_elem else None,
                        'year': self.clean_text(year_elem.text) if year_elem else None,
                        'format': self.clean_text(format_elem.text) if format_elem else None,
                        'size': self.clean_size(size_elem.text) if size_elem else None,
                        'language': self.clean_text(language_elem.text) if language_elem else None,
                        'url': urljoin(self.base_url, title_elem.find('a')['href']) if title_elem and title_elem.find('a') else None
                    }
                    
                    self.books_data.append(book_data)
                    logging.info(f"Scraped book: {book_data['title']}")

                except AttributeError as e:
                    logging.error(f"Error parsing book data: {str(e)}")
                    continue

            return len(books) > 0

        except requests.RequestException as e:
            logging.error(f"Error fetching search results: {str(e)}")
            return False

    def save_to_csv(self, filename=None):
        if not self.books_data:
            logging.warning("No data to save")
            return None

        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'zlibrary_books_{timestamp}.csv'
        
        try:
            df = pd.DataFrame(self.books_data)
            df.to_csv(filename, index=False, encoding='utf-8')
            logging.info(f"Data successfully saved to {filename}")
            return filename
        except Exception as e:
            logging.error(f"Error saving data to CSV: {str(e)}")
            return None

def main():
    scraper = ZLibraryScraper()
    
    print("Welcome to the Z-Library Scraper!")
    search_query = input("Enter search term: ").strip()
    max_results = int(input("Enter maximum number of books to scrape (1-100): ").strip())
    max_results = min(max(1, max_results), 100)
    
    print(f"\nSearching for '{search_query}'...")
    page = 1
    while True:
        print(f"Scraping page {page}...")
        if not scraper.search_books(search_query, page, max_results):
            break
        if len(scraper.books_data) >= max_results:
            break
        page += 1
        time.sleep(2)  # Polite delay between requests
    
    if scraper.books_data:
        filename = scraper.save_to_csv()
        if filename:
            print(f"\nData successfully saved to {filename}")
            print(f"Total books scraped: {len(scraper.books_data)}")
        else:
            print("Error saving data to CSV file")
    else:
        print("No books found matching your search criteria")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScraping interrupted by user")
        logging.info("Scraping interrupted by user")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        logging.error(f"Unexpected error: {str(e)}")