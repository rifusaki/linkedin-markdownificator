from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import time
import pathlib
import os

# Do not forget to modify .env
load_dotenv()

# Make (or use) a '/selenium' folder user profile to preserve session cookies
# It's also possible to manage extensions, settings... per user basis
options = Options()
options.add_argument(f"user-data-dir={pathlib.Path().absolute()}\\selenium")
driver = webdriver.Chrome(options=options)

driver.get("https://linkedin.com/")
driver.implicitly_wait(5)

# LinkedIn when logged in redirects to feed. If not logged, login elements should be available in main page
if "feed" not in driver.title.lower():
    print("login required")
    driver.find_element(by=By.ID, value="session_key").send_keys(os.getenv("MAIL"))
    driver.find_element(by=By.ID, value="session_password").send_keys(os.getenv("PASSWORD"), Keys.ENTER)
    driver.implicitly_wait(30) # Increase time if needed for captcha

elif "feed" in driver.title.lower():
    print("session cookie preserved")
    
driver.implicitly_wait(15)
driver.find_element(By.XPATH, "//a[contains(@href, '/in/')]").click()
print("profile loaded")

driver.quit()