from selenium import webdriver
from selenium.webdriver.common.by import By

# Use raw string (r) or double backslashes for the path
PATH = r"C:\Program Files\chromedriver\chromedriver.exe"

# Initialize the WebDriver
driver = webdriver.Chrome(PATH)

# Open a website
driver.get("https://www.like4like.org/login/")

# Locate the username field (modify 'username' to match the actual ID on the page you're testing)
username = driver.find_element(By.ID, 'username')
username.send_keys("hello")

# Close the browser after use
driver.quit()
