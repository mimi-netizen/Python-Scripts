from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup Chrome options
chrome_options = Options()
# chrome_options.add_argument('--headless')  # Uncomment to run headless

# Create Service object
service = Service('/usr/bin/chromedriver')  # Adjust path as needed

# Initialize WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds for elements

try:
    # Navigate to the login page
    driver.get("https://www.like4like.org/login/")
    
    # Wait for page to load
    time.sleep(2)
    
    # Find username field using XPath
    username = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@name='username' or @id='username']")))
    username.clear()
    username.send_keys("your_username")
    
    # Find password field using XPath
    password = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@type='password']")))
    password.clear()
    password.send_keys("your_password")
    
    # Find and click login button using XPath
    login_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@type='submit' or @value='Submit']")))
    login_button.click()
    
    # Wait for login to complete
    time.sleep(3)
    
    # Optional: Verify successful login by checking for an element that appears after login
    try:
        success_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[contains(@class,'success-message')]")))
        print("Login successful!")
    except:
        print("Login verification failed or timeout occurred")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()