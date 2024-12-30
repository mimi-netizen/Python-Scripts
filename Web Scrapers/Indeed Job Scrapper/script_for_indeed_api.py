import requests
import pandas as pd
from pathlib import Path
import smtplib
import logging
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from datetime import datetime
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv
import json
from dataclasses import dataclass
from requests.exceptions import RequestException
import time

# Load environment variables
load_dotenv()

# Configuration
BASE_DIR = Path(__file__).parent / 'job_data'
LOG_DIR = BASE_DIR / 'logs'
OUTPUT_DIR = BASE_DIR / 'reports'

# Create necessary directories
for directory in [BASE_DIR, LOG_DIR, OUTPUT_DIR]:
    directory.mkdir(exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / 'job_scraper.log'),
        logging.StreamHandler()
    ]
)

@dataclass
class EmailConfig:
    sender: str
    recipients: List[str]
    subject: str
    body: str
    smtp_server: str
    smtp_port: int
    username: str
    password: str

class IndeedJobAPI:
    def __init__(self):
        self.api_key = os.getenv('INDEED_API_KEY')
        if not self.api_key:
            raise ValueError("Indeed API key not found in environment variables")
        
        self.base_url = 'https://api.indeed.com/ads/apisearch'
        self.session = requests.Session()

    def get_job_postings(self, query: str = 'remote', location: str = '', 
                        max_results: int = 25) -> List[Dict]:
        """Fetch job postings from Indeed API with rate limiting and error handling."""
        params = {
            'q': query,
            'l': location,
            'format': 'json',
            'v': '2',
            'limit': max_results,
            'publisher': self.api_key,
        }

        try:
            response = self.session.get(
                url=self.base_url,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            # Rate limiting
            time.sleep(1)
            
            return response.json().get('results', [])
            
        except RequestException as e:
            logging.error(f"API request failed: {str(e)}")
            return []
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse API response: {str(e)}")
            return []

class JobDataExporter:
    @staticmethod
    def to_excel(data: List[Dict], filename: Optional[str] = None) -> Path:
        """Export job data to Excel file."""
        if not data:
            raise ValueError("No data to export")

        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'indeed_jobs_{timestamp}.xlsx'
        
        output_path = OUTPUT_DIR / filename
        
        try:
            # Export to Excel with proper formatting
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Jobs', index=False)
                
                # Auto-adjust columns width
                worksheet = writer.sheets['Jobs']
                for idx, col in enumerate(df.columns):
                    max_length = max(
                        df[col].astype(str).apply(len).max(),
                        len(col)
                    )
                    worksheet.column_dimensions[chr(65 + idx)].width = max_length + 2
                    
            logging.info(f"Data exported to {output_path}")
            return output_path
            
        except Exception as e:
            logging.error(f"Failed to export data: {str(e)}")
            raise

class EmailSender:
    def __init__(self, config: EmailConfig):
        self.config = config

    def send_email(self, attachments: List[Path] = None) -> bool:
        """Send email with attachments."""
        msg = MIMEMultipart()
        msg['From'] = self.config.sender
        msg['To'] = COMMASPACE.join(self.config.recipients)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = self.config.subject

        msg.attach(MIMEText(self.config.body))

        # Attach files
        for attachment in attachments or []:
            try:
                with open(attachment, "rb") as f:
                    part = MIMEApplication(f.read(), Name=attachment.name)
                part['Content-Disposition'] = f'attachment; filename="{attachment.name}"'
                msg.attach(part)
            except Exception as e:
                logging.error(f"Failed to attach file {attachment}: {str(e)}")
                return False

        # Send email
        try:
            with smtplib.SMTP(self.config.smtp_server, self.config.smtp_port) as smtp:
                smtp.starttls()
                smtp.login(self.config.username, self.config.password)
                smtp.sendmail(self.config.sender, self.config.recipients, msg.as_string())
            logging.info("Email sent successfully")
            return True
            
        except Exception as e:
            logging.error(f"Failed to send email: {str(e)}")
            return False

def main():
    try:
        # Initialize Indeed API client
        indeed_client = IndeedJobAPI()
        
        # Fetch job postings
        jobs = indeed_client.get_job_postings(
            query='python developer',
            location='remote',
            max_results=50
        )
        
        if not jobs:
            logging.warning("No jobs found")
            return
            
        # Export to Excel
        exporter = JobDataExporter()
        excel_file = exporter.to_excel(jobs)
        
        # Send email
        email_config = EmailConfig(
            sender=os.getenv('EMAIL_SENDER'),
            recipients=os.getenv('EMAIL_RECIPIENTS', '').split(','),
            subject='Latest Job Postings Report',
            body='Please find attached the latest job postings report.',
            smtp_server=os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
            smtp_port=int(os.getenv('SMTP_PORT', '587')),
            username=os.getenv('EMAIL_USERNAME'),
            password=os.getenv('EMAIL_PASSWORD')
        )
        
        email_sender = EmailSender(email_config)
        email_sent = email_sender.send_email([excel_file])
        
        if email_sent:
            logging.info("Process completed successfully")
        else:
            logging.error("Process completed with errors")
            
    except Exception as e:
        logging.error(f"Process failed: {str(e)}")

if __name__ == "__main__":
    main()