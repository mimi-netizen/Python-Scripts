# You are tasked with scraping job listings from a job portal (e.g., Indeed or LinkedIn). Your goal is to extract the following information for each job listing:

# Job Title

# Company Name

# Location

# Job Description

# Using BeautifulSoup and Python, write a script to scrape this information from the first three pages of job listings. Ensure that your solution handles potential errors, such as network issues or changes in the website structure.


# URL of the job portal (e.g., Indeed)

import requests
from bs4 import BeautifulSoup
import time

# URL of the job portal (e.g., Indeed)
base_url = 'https://www.indeed.com/jobs?q=software+developer&l='

# Function to fetch job listings from a page
def fetch_job_listings(page_number):
    url = base_url + f'&start={page_number * 10}'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Send HTTP request to the URL
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check if the request was successful
        
        # Parse the page content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all job cards on the page
        job_cards = soup.find_all('div', class_='job_seen_beacon')  # Updated class

        jobs = []

        for job_card in job_cards:
            # Extract job title
            job_title = job_card.find('h2', class_='jobTitle')  # Updated tag and class
            job_title = job_title.text.strip() if job_title else 'N/A'

            # Extract company name
            company = job_card.find('span', class_='companyName')  # Updated class
            company = company.text.strip() if company else 'N/A'

            # Extract location
            location = job_card.find('div', class_='companyLocation')  # Updated class
            location = location.text.strip() if location else 'N/A'

            # Extract job description (or job snippet)
            job_description = job_card.find('div', class_='job-snippet')  # Updated class
            job_description = job_description.text.strip() if job_description else 'N/A'

            # Store the extracted data
            jobs.append({
                'Job Title': job_title,
                'Company': company,
                'Location': location,
                'Job Description': job_description
            })

        return jobs

    except requests.RequestException as e:
        print(f"Error fetching page {page_number + 1}: {e}")
        return []

# Main function to scrape the first 3 pages
def scrape_job_listings():
    all_jobs = []

    for page_number in range(3):  # First 3 pages (0-based index)
        print(f"Scraping page {page_number + 1}...")
        jobs = fetch_job_listings(page_number)

        if jobs:
            all_jobs.extend(jobs)
        else:
            print(f"No jobs found on page {page_number + 1} or error occurred.")

        time.sleep(2)  # Sleep for 2 seconds between requests

    # Output the scraped job listings
    for idx, job in enumerate(all_jobs, 1):
        print(f"\nJob {idx}:")
        print(f"Title: {job['Job Title']}")
        print(f"Company: {job['Company']}")
        print(f"Location: {job['Location']}")
        print(f"Description: {job['Job Description']}")
        print('-' * 80)

# Run the scraper
scrape_job_listings()