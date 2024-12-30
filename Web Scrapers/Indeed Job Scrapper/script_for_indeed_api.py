import requests
import xlwt
from xlwt import Workbook
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import getpass
from datetime import datetime

API_KEY = 'your_indeed_api_key'
BASE_URL = 'https://api.indeed.com/ads/apisearch'
REQUEST_PARAMS = {
    'q': 'remote',
    'l': '',
    'format': 'json',
    'v': '2',
    'publisher': API_KEY,
}

def get_job_postings():
    try:
        res = requests.get(url=BASE_URL, params=REQUEST_PARAMS)
        res.raise_for_status()
        return res.json().get('results', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

def output_jobs_to_xls(data):
    wb = Workbook()
    job_sheet = wb.add_sheet('Jobs')
    headers = list(data[0].keys())
    for i in range(len(headers)):
        job_sheet.write(0, i, headers[i])
    for i in range(len(data)):
        job = data[i]
        values = list(job.values())
        for x in range(len(values)):
            job_sheet.write(i + 1, x, values[x])
    filename = f'indeed_jobs_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xls'
    wb.save(filename)
    return filename

def send_email(send_from, send_to, subject, text, files=None):
    assert isinstance(send_to, list)
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(fil.read(), Name=basename(f))
        part['Content-Disposition'] = f'attachment; filename="{basename(f)}"'
        msg.attach(part)

    try:
        smtp = smtplib.SMTP('smtp.gmail.com: 587')
        smtp.starttls()
        smtp.login(send_from, getpass.getpass("Enter your email password: "))
        smtp.sendmail(send_from, send_to, msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        smtp.close()

if __name__ == "__main__":
    json_data = get_job_postings()
    if json_data:
        filename = output_jobs_to_xls(json_data)
        send_email('your email', ['recipient email'], 'Jobs Posting', 'Please, find attached a list of job postings.', files=[filename])