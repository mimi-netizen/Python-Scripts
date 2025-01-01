from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Setup Chrome options
chrome_options = Options()
# Add options if needed
# chrome_options.add_argument('--headless')  # Run in headless mode if desired

# Create a Service object
# For Linux/WSL, use the appropriate path
service = Service('/usr/bin/chromedriver')  # Adjust path as needed

# Initialize the WebDriver with the service and options
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Open the website
    driver.get("https://www.like4like.org/login/")

    # Locate the username field
    username = driver.find_element(By.ID, 'username')
    username.send_keys("hello")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()