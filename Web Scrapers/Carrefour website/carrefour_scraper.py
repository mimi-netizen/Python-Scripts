from datetime import datetime
import requests
import csv
import bs4
from typing import Dict, Optional, Any
import time
import logging
from pathlib import Path
import concurrent.futures
from requests.exceptions import RequestException

# Configuration
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
HEADERS = {
    'User-Agent': USER_AGENT,
    'Accept-Language': 'en-US, en;q=0.5',
}
REQUEST_TIMEOUT = 30
RETRY_ATTEMPTS = 3
DELAY_BETWEEN_REQUESTS = 1  # seconds
MAX_WORKERS = 5  # for parallel processing

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)

class ProductScraper:
    def __init__(self, input_file: str, output_dir: str = 'output'):
        self.input_file = Path(input_file)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def get_page_html(self, url: str) -> Optional[str]:
        for attempt in range(RETRY_ATTEMPTS):
            try:
                response = self.session.get(url, timeout=REQUEST_TIMEOUT)
                response.raise_for_status()
                return response.text
            except RequestException as e:
                logging.error(f"Attempt {attempt + 1} failed for URL {url}: {str(e)}")
                if attempt == RETRY_ATTEMPTS - 1:
                    return None
                time.sleep(DELAY_BETWEEN_REQUESTS * (attempt + 1))
        return None

    @staticmethod
    def get_product_price(soup: bs4.BeautifulSoup) -> Optional[float]:
        try:
            price_span = soup.find('span', class_='price')
            if price_span:
                price_text = price_span.text.strip()
                price = ''.join(filter(str.isdigit, price_text))
                return float(price) if price else None
        except (ValueError, AttributeError) as e:
            logging.error(f"Error parsing price: {str(e)}")
        return None

    @staticmethod
    def get_product_title(soup: bs4.BeautifulSoup) -> Optional[str]:
        try:
            title = soup.find('h1', class_='product-title')
            return title.text.strip() if title else None
        except AttributeError as e:
            logging.error(f"Error parsing title: {str(e)}")
            return None

    @staticmethod
    def get_product_rating(soup: bs4.BeautifulSoup) -> Optional[float]:
        try:
            rating_div = soup.find('div', class_='rating')
            if rating_div:
                rating_span = rating_div.find('span')
                return float(rating_span.text.strip()) if rating_span else None
        except (ValueError, AttributeError) as e:
            logging.error(f"Error parsing rating: {str(e)}")
        return None

    def extract_product_info(self, url: str) -> Dict[str, Any]:
        product_info = {
            'url': url,
            'price': None,
            'title': None,
            'rating': None,
            'timestamp': datetime.now().isoformat()
        }
        
        logging.info(f'Scraping URL: {url}')
        html = self.get_page_html(url)
        
        if not html:
            logging.error(f"Failed to fetch HTML for URL: {url}")
            return product_info

        soup = bs4.BeautifulSoup(html, 'lxml')
        product_info['price'] = self.get_product_price(soup)
        product_info['title'] = self.get_product_title(soup)
        product_info['rating'] = self.get_product_rating(soup)
        
        time.sleep(DELAY_BETWEEN_REQUESTS)  # Rate limiting
        return product_info

    def process_urls(self) -> list:
        urls = []
        try:
            with open(self.input_file, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                urls = [row[0] for row in reader]
        except Exception as e:
            logging.error(f"Error reading input file: {str(e)}")
            return []

        products_data = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_url = {executor.submit(self.extract_product_info, url): url 
                           for url in urls}
            
            for future in concurrent.futures.as_completed(future_to_url):
                try:
                    data = future.result()
                    products_data.append(data)
                except Exception as e:
                    url = future_to_url[future]
                    logging.error(f"Error processing {url}: {str(e)}")

        return products_data

    def save_to_csv(self, products_data: list) -> None:
        if not products_data:
            logging.warning("No data to save")
            return

        output_file = self.output_dir / f'output-{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=products_data[0].keys())
                writer.writeheader()
                writer.writerows(products_data)
            logging.info(f"Data saved to {output_file}")
        except Exception as e:
            logging.error(f"Error saving data: {str(e)}")

def main():
    scraper = ProductScraper('carrefour_products_urls.csv')
    products_data = scraper.process_urls()
    scraper.save_to_csv(products_data)

if __name__ == "__main__":
    main()