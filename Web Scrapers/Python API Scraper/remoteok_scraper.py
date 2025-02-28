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

BASE_URL = 'https://remoteok.com/api/'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0'
REQUEST_HEADER = {
    'User-Agent': USER_AGENT,
    'Accept-Language': 'en-US, en;q=0.5',
}

def get_job_postings():
    try:
        res = requests.get(url=BASE_URL, headers=REQUEST_HEADER)
        res.raise_for_status()
        return res.json()
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
    filename = f'remote_jobs_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xls'
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
    json_data = get_job_postings()[1:]
    if json_data:
        filename = output_jobs_to_xls(json_data)
        send_email('your email', ['recipient email'], 'Jobs Posting', 'Please, find attached a list of job postings.', files=[filename])