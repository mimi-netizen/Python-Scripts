from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from datetime import datetime
import os
import json
import logging
import sys

class TrelloBot:
    def __init__(self):
        self.setup_logging()
        self.load_config()
        self.setup_driver()
        self.wait = WebDriverWait(self.driver, 20)

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('trello_bot.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def load_config(self):
        try:
            with open('config.json') as config_file:
                self.config = json.load(config_file)
        except FileNotFoundError:
            self.logger.error("Config file not found")
            sys.exit(1)
        except json.JSONDecodeError:
            self.logger.error("Invalid JSON in config file")
            sys.exit(1)

    def setup_driver(self):
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.maximize_window()
        except WebDriverException as e:
            self.logger.error(f"Failed to initialize WebDriver: {e}")
            sys.exit(1)

    def wait_and_find_element(self, by, value):
        try:
            element = self.wait.until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            self.logger.error(f"Element not found: {value}")
            raise

    def take_screenshot(self):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshots_dir = os.path.join(os.getcwd(), 'screenshots')
            os.makedirs(screenshots_dir, exist_ok=True)
            
            filepath = os.path.join(screenshots_dir, f'trello_{timestamp}.png')
            self.driver.save_screenshot(filepath)
            self.logger.info(f"Screenshot saved: {filepath}")
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {e}")

    def add_task(self, task_text="Bot Added Task"):
        try:
            # Click on "Add a card" button
            add_card_button = self.wait_and_find_element(
                By.XPATH,
                "//textarea[@aria-label='To Do']/ancestor::div/descendant::div[@class='card-composer-container js-card-composer-container']/child::a"
            )
            add_card_button.click()

            # Enter task text
            task_textarea = self.wait_and_find_element(
                By.XPATH,
                "//div[@class='card-composer']/descendant::textarea"
            )
            task_textarea.clear()
            task_textarea.send_keys(task_text)

            # Submit new task
            submit_button = self.wait_and_find_element(
                By.XPATH,
                "//input[@value='Add card']"
            )
            submit_button.click()
            
            self.logger.info(f"Successfully added task: {task_text}")
        except Exception as e:
            self.logger.error(f"Failed to add task: {e}")
            raise

    def login(self):
        try:
            self.driver.get("https://id.atlassian.com/login?application=trello&continue=https%3A%2F%2Ftrello.com%2Fauth%2Fatlassian%2Fcallback%3Fdisplay%3DeyJ2ZXJpZmljYXRpb25TdHJhdGVneSI6InNvZnQifQ%253D%253D&display=eyJ2ZXJpZmljYXRpb25TdHJhdGVneSI6InNvZnQifQ%3D%3D")
            
            # Click login button
            login_button = self.wait_and_find_element(By.XPATH, "//*[@id='login-submit']")
            login_button.click()

            # Enter username
            username_field = self.wait_and_find_element(By.CSS_SELECTOR, "input[name='user']")
            username_field.send_keys(self.config["USERNAME"])

            # Enter password and submit
            password_field = self.wait_and_find_element(By.CSS_SELECTOR, "input[name='password']")
            password_field.send_keys(self.config["PASSWORD"])
            
            submit_button = self.wait_and_find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_button.click()
            
            self.logger.info("Successfully logged in")
        except Exception as e:
            self.logger.error(f"Login failed: {e}")
            raise

    def navigate_to_board(self, board_name='Bot Board'):
        try:
            board = self.wait_and_find_element(
                By.XPATH,
                f"//div[@title='{board_name}']/ancestor::a"
            )
            board.click()
            self.logger.info(f"Navigated to board: {board_name}")
        except Exception as e:
            self.logger.error(f"Failed to navigate to board: {e}")
            raise

    def run(self):
        try:
            self.login()
            self.navigate_to_board()
            self.add_task()
            self.take_screenshot()
            self.logger.info("Bot operations completed successfully")
        except Exception as e:
            self.logger.error(f"Bot operation failed: {e}")
        finally:
            self.driver.quit()

if __name__ == "__main__":
    bot = TrelloBot()
    bot.run()