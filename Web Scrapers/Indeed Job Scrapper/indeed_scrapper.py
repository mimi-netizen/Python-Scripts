# You are tasked with scraping job listings from a job portal (e.g., Indeed or LinkedIn). Your goal is to extract the following information for each job listing:

# Job Title

# Company Name

# Location

# Job Description

# Using BeautifulSoup and Python, write a script to scrape this information from the first three pages of job listings. Ensure that your solution handles potential errors, such as network issues or changes in the website structure.


import requests
from bs4 import BeautifulSoup
import time
import logging
import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass
from pathlib import Path
import json
from requests.exceptions import RequestException
import os

# Configuration
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Create base directory
SCRIPT_DIR = Path(__file__).parent
BASE_DIR = SCRIPT_DIR / 'job_scraper_data'
BASE_DIR.mkdir(exist_ok=True)

# Create log directory
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / 'scraper.log'),
        logging.StreamHandler()
    ]
)

@dataclass
class JobListing:
    title: str
    company: str
    location: str
    description: str
    url: str
    date_posted: Optional[str] = None
    salary: Optional[str] = None
    job_type: Optional[str] = None

class JobScraper:
    def __init__(self, base_url: str, search_query: str, location: str = ''):
        self.base_url = base_url
        self.search_query = search_query
        self.location = location
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        
        # Create directory for data storage
        self.data_dir = BASE_DIR / 'data'
        self.data_dir.mkdir(exist_ok=True)
        
    def _build_url(self, page_number: int) -> str:
        """Construct the URL for a specific page number."""
        return f"{self.base_url}jobs?q={self.search_query}&l={self.location}&start={page_number * 10}"

    def _fetch_page(self, url: str) -> Optional[str]:
        """Fetch page content with error handling."""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            time.sleep(3)  # Simple rate limiting
            return response.text
        except RequestException as e:
            logging.error(f"Error fetching URL {url}: {str(e)}")
            return None

    def _parse_job_card(self, card: BeautifulSoup) -> Optional[JobListing]:
        """Parse a single job card and return a JobListing object."""
        try:
            # Extract basic information with error handling
            title_elem = card.find('h2', class_='jobTitle')
            company_elem = card.find('span', class_='companyName')
            location_elem = card.find('div', class_='companyLocation')
            description_elem = card.find('div', class_='job-snippet')
            
            # Get URL if available
            url_elem = card.find('a', class_='jcs-JobTitle')
            url = f"{self.base_url}{url_elem['href']}" if url_elem and 'href' in url_elem.attrs else ''
            
            # Additional information (if available)
            date_posted = card.find('span', class_='date')
            salary = card.find('div', class_='salary-snippet')
            job_type = card.find('div', class_='metadata job-type')

            return JobListing(
                title=title_elem.text.strip() if title_elem else 'N/A',
                company=company_elem.text.strip() if company_elem else 'N/A',
                location=location_elem.text.strip() if location_elem else 'N/A',
                description=description_elem.text.strip() if description_elem else 'N/A',
                url=url,
                date_posted=date_posted.text.strip() if date_posted else None,
                salary=salary.text.strip() if salary else None,
                job_type=job_type.text.strip() if job_type else None
            )
        except Exception as e:
            logging.error(f"Error parsing job card: {str(e)}")
            return None

    def _parse_page(self, html: str) -> List[JobListing]:
        """Parse the page HTML and extract job listings."""
        soup = BeautifulSoup(html, 'html.parser')
        job_cards = soup.find_all('div', class_='job_seen_beacon')
        
        jobs = []
        for card in job_cards:
            job = self._parse_job_card(card)
            if job:
                jobs.append(job)
        
        return jobs

    def scrape_jobs(self, num_pages: int = 3) -> List[JobListing]:
        """Scrape job listings from the specified number of pages."""
        all_jobs = []
        
        for page in range(num_pages):
            logging.info(f"Scraping page {page + 1}/{num_pages}")
            
            url = self._build_url(page)
            html = self._fetch_page(url)
            
            if not html:
                logging.error(f"Failed to fetch page {page + 1}")
                continue
                
            jobs = self._parse_page(html)
            all_jobs.extend(jobs)
            
            logging.info(f"Found {len(jobs)} jobs on page {page + 1}")
            
        return all_jobs

    def save_results(self, jobs: List[JobListing]) -> None:
        """Save the scraped results in multiple formats."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save as CSV
        df = pd.DataFrame([vars(job) for job in jobs])
        df.to_csv(self.data_dir / f'jobs_{timestamp}.csv', index=False)
        
        # Save as JSON
        with open(self.data_dir / f'jobs_{timestamp}.json', 'w') as f:
            json.dump([vars(job) for job in jobs], f, indent=2)
            
        logging.info(f"Saved {len(jobs)} job listings to files with timestamp {timestamp}")

def main():
    # Example usage
    scraper = JobScraper(
        base_url='https://www.indeed.com/',
        search_query='software+developer',
        location='remote'
    )
    
    try:
        jobs = scraper.scrape_jobs(num_pages=3)
        scraper.save_results(jobs)
        
        # Print summary
        print(f"\nScraping Summary:")
        print(f"Total jobs found: {len(jobs)}")
        print(f"Unique companies: {len(set(job.company for job in jobs))}")
        print(f"Unique locations: {len(set(job.location for job in jobs))}")
        
    except Exception as e:
        logging.error(f"Error during scraping: {str(e)}")

if __name__ == "__main__":
    main()