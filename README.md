# Python Scripts Collection

A comprehensive collection of Python scripts focusing on Web Automation, Web Scraping, and Cryptography implementations. This repository serves as a resource for developers interested in automation, data extraction, and security.

## 🌟 Projects Overview

### 1. Selenium Web Automation

Advanced web automation scripts using Selenium WebDriver for various platforms and applications.

#### Key Features

- **Email Automation**: Automated email tasks and inbox management
- **Social Media Automation**:
  - Facebook interactions
  - WhatsApp messaging
  - Telegram bot functionality
  - YouTube automation
- **Task Management**:
  - Trello board automation
  - Project workflow automation
- **Locator Strategies**:
  - XPath implementations
  - CSS Selector examples
  - Practical automation templates

### 2. Web Scrapers

Collection of Python web scraping scripts for automated data extraction from various websites.

#### Key Features

- **Specialized Scrapers**:
  - Books information extractor
  - Carrefour website product scraper
  - IMDB movie/TV show data collector
  - Indeed job listings extractor
  - General HTML scraper
  - API data extractor
- **Data Extraction Capabilities**:
  - Product information
  - Pricing details
  - Description extraction
  - Rating systems
  - User reviews

### 3. Cryptography

Implementation of various cryptographic algorithms and security concepts.

#### Current Implementations

- Types of Ciphers
- Public Key Cryptography
- Hash Functions
- Message Authentication Codes (MAC, CMAC, HMAC)
- Digital Certificates
- Authentication Systems
- TCP/IP Security
- Internet Security Protocols
- Firewall Implementation
- Intrusion Detection System
- Network Security Concepts

## 🛠️ Technical Requirements

### General Requirements

- Python 3.x
- Git

### Project-Specific Dependencies

#### Selenium Web Automation

```bash
pip install selenium webdriver_manager
```

#### Web Scrapers

```bash
pip install requests beautifulsoup4
```

#### Cryptography

```bash
pip install pycryptodome
```

## 📦 Installation

1. Clone the repository

```bash
git clone https://github.com/mimi-netizen/Python-Scripts.git
```

2. Navigate to the project directory

```bash
cd Python-Scripts
```

3. Install required dependencies

```bash
pip install -r requirements.txt
```

## 🚀 Usage

### Selenium Web Automation

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Setup Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
```

### Web Scrapers

```python
import requests
from bs4 import BeautifulSoup

# Basic scraping template
response = requests.get('https://example.com')
soup = BeautifulSoup(response.text, 'html.parser')
```

### Cryptography

```python
# Example cipher implementation
def caesar_cipher(text, shift, encrypt=True):
    result = ""
    for char in text:
        if char.isalpha():
            ascii_offset = ord('A') if char.isupper() else ord('a')
            shift_value = shift if encrypt else -shift
            result += chr((ord(char) - ascii_offset + shift_value) % 26 + ascii_offset)
        else:
            result += char
    return result
```

## 🔍 Monitoring and Logging

### Selenium Projects

All Selenium projects create logs in `logs/selenium/`:

```
tail -f logs/selenium/automation.log
```

### Web Scrapers

Monitor scraping progress:

```bash
tail -f logs/scrapers/scraping_progress.log
```

Rate limiting and error logs:

```bash
cat logs/scrapers/rate_limits.log
cat logs/scrapers/errors.log
```

### Cryptography

Operation logs and performance metrics:

```bash
cat logs/crypto/operations.log
cat logs/crypto/performance_metrics.log
```

## 🐛 Debugging Tips

### Selenium Debugging

- Enable verbose logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

- Use Chrome DevTools:

```python
chrome_options.add_argument('--auto-open-devtools-for-tabs')
```

### Web Scraper Debugging

- Test selectors in browser console
- Use `scrapy shell` for interactive debugging:

```bash
scrapy shell "http://example.com"
```

### Cryptography Debugging

- Enable verbose mode:

```bash
python crypto_script.py --verbose
```

- Use test vectors in `tests/vectors/` directory

## 🐛 Advanced Debugging Guide

### 1. Selenium Debugging Techniques

#### Basic Logging Setup

```python
import logging

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)

# Create a custom logger
logger = logging.getLogger('selenium_automation')
```

#### Screenshot Capture

```python
def capture_error_screenshot(driver, error_name):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshot_path = f"debug/screenshots/{error_name}_{timestamp}.png"
    driver.save_screenshot(screenshot_path)
    logger.debug(f"Screenshot saved: {screenshot_path}")

# Usage in try-except block
try:
    element = driver.find_element(By.ID, "submit-button")
    element.click()
except Exception as e:
    capture_error_screenshot(driver, "click_error")
    logger.error(f"Click failed: {str(e)}")
```

#### Element State Debugging

```python
def debug_element(driver, locator, by=By.CSS_SELECTOR):
    try:
        element = driver.find_element(by, locator)
        debug_info = {
            "is_displayed": element.is_displayed(),
            "is_enabled": element.is_enabled(),
            "is_selected": element.is_selected(),
            "location": element.location,
            "size": element.size,
            "class": element.get_attribute("class"),
            "computed_style": driver.execute_script(
                "return window.getComputedStyle(arguments[0]);",
                element
            )
        }
        logger.debug(f"Element debug info: {debug_info}")
        return debug_info
    except Exception as e:
        logger.error(f"Element debugging failed: {str(e)}")
```

#### Network Traffic Monitoring

```python
from selenium.webdriver.chrome.options import Options

def setup_network_debugging():
    chrome_options = Options()
    chrome_options.set_capability(
        "goog:loggingPrefs",
        {"performance": "ALL", "browser": "ALL"}
    )
    return chrome_options

def analyze_network_logs(driver):
    logs = driver.get_log("performance")
    for log in logs:
        network_log = json.loads(log["message"])["message"]
        if "Network.responseReceived" in network_log["method"]:
            logger.debug(f"Network response: {network_log}")
```

### 2. Web Scraper Debugging

#### Request Inspection

```python
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

def debug_request(url, headers=None):
    session = requests.Session()
    retries = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=[500, 502, 503, 504]
    )
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))

    try:
        response = session.get(url, headers=headers)
        debug_info = {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "cookies": dict(response.cookies),
            "encoding": response.encoding,
            "redirect_history": [
                {"url": r.url, "status_code": r.status_code}
                for r in response.history
            ]
        }
        logger.debug(f"Request debug info: {debug_info}")
        return debug_info
    except Exception as e:
        logger.error(f"Request failed: {str(e)}")
```

#### HTML Parser Debugging

```python
from bs4 import BeautifulSoup
import lxml.html

def debug_parsing(html_content):
    # BeautifulSoup parsing
    soup = BeautifulSoup(html_content, 'html.parser')

    # Compare with lxml parsing
    lxml_doc = lxml.html.fromstring(html_content)

    debug_info = {
        "soup_title": soup.title.string if soup.title else None,
        "lxml_title": lxml_doc.find(".//title").text if lxml_doc.find(".//title") is not None else None,
        "soup_encoding": soup.original_encoding,
        "tags_count": len(soup.find_all()),
        "broken_tags": soup.find_all(lambda tag: tag.name is None)
    }

    logger.debug(f"Parsing debug info: {debug_info}")
    return debug_info
```

### 3. Cryptography Debugging

#### Key Generation Debugging

```python
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

def debug_key_generation(key_size=2048):
    try:
        start_time = time.time()
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size
        )
        generation_time = time.time() - start_time

        # Analyze key properties
        debug_info = {
            "key_size": key_size,
            "generation_time": generation_time,
            "public_numbers": {
                "n": private_key.public_key().public_numbers().n,
                "e": private_key.public_key().public_numbers().e
            },
            "private_numbers": {
                "p": private_key.private_numbers().p,
                "q": private_key.private_numbers().q,
                "d": private_key.private_numbers().d
            }
        }

        logger.debug(f"Key generation debug info: {debug_info}")
        return debug_info
    except Exception as e:
        logger.error(f"Key generation failed: {str(e)}")
```

#### Encryption Process Debugging

```python
def debug_encryption_process(data, key):
    try:
        debug_info = {
            "input_data": {
                "length": len(data),
                "encoding": chardet.detect(data)
            },
            "key_info": {
                "algorithm": key.algorithm.name,
                "key_size": key.key_size
            }
        }

        # Track encryption steps
        padded_data = pad(data)
        debug_info["padding"] = {
            "original_length": len(data),
            "padded_length": len(padded_data)
        }

        # Monitor encryption performance
        start_time = time.time()
        encrypted_data = encrypt(padded_data, key)
        debug_info["encryption_time"] = time.time() - start_time

        logger.debug(f"Encryption debug info: {debug_info}")
        return encrypted_data, debug_info
    except Exception as e:
        logger.error(f"Encryption failed: {str(e)}")
```

#### Memory Usage Monitoring

```python
import psutil
import os

def monitor_memory_usage():
    process = psutil.Process(os.getpid())
    memory_info = {
        "rss": process.memory_info().rss / 1024 / 1024,  # MB
        "vms": process.memory_info().vms / 1024 / 1024,  # MB
        "percent": process.memory_percent(),
        "cpu_percent": process.cpu_percent()
    }
    logger.debug(f"Memory usage: {memory_info}")
    return memory_info

# Usage example
def process_large_file(file_path):
    initial_memory = monitor_memory_usage()

    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                process_chunk(chunk)
                current_memory = monitor_memory_usage()

                if current_memory["percent"] > 90:
                    logger.warning("High memory usage detected!")

    except Exception as e:
        logger.error(f"File processing failed: {str(e)}")

    final_memory = monitor_memory_usage()
    logger.debug(f"Memory change: {final_memory['rss'] - initial_memory['rss']} MB")
```

## 🔄 Common Issues and Solutions

### Selenium

- ChromeDriver version mismatch: Update using `webdriver_manager`
- Element not found: Implement explicit waits
- Stale elements: Refresh page or relocate element

### Web Scrapers

- Rate limiting: Implement delays between requests
- IP blocks: Rotate proxies using `proxy_rotator.py`
- Dynamic content: Use Selenium for JavaScript-heavy sites

### Cryptography

- Key generation errors: Check system entropy
- Performance issues: Use appropriate key sizes
- Memory errors: Implement streaming for large files

## 📚 Documentation

Each project contains its own detailed documentation:

- [Selenium Web Automation Documentation](./Selenium%20Web%20Automation/README.md)
- [Web Scrapers Documentation](./Web%20Scrapers/README.md)
- [Cryptography Documentation](./cryptography/README.md)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

Celyne Kydd - celynekydd@gmail.com

Project Link: [https://github.com/mimi-netizen/Python-Scripts](https://github.com/mimi-netizen/Python-Scripts)

## 🙏 Acknowledgments

- Selenium Documentation
- BeautifulSoup Documentation
- Cryptography Libraries and Resources
- Python Community
