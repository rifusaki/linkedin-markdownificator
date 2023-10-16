from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import pathlib
import os

load_dotenv()

options = Options()
options.add_argument(f"user-data-dir={pathlib.Path().absolute()}\\selenium")
driver = webdriver.Chrome(options=options)
driver.get("https://co.linkedin.com/")
driver.implicitly_wait(5)

if "feed" not in driver.title.lower():
    print("login required")
    driver.find_element(by=By.ID, value="session_key").send_keys(os.getenv("MAIL"))
    password = driver.find_element(by=By.ID, value="session_password")
    password.send_keys(os.getenv("PASSWORD"), Keys.ENTER)
    driver.implicitly_wait(30)
elif "feed" in driver.title.lower():
    print("session cookie preserved")

driver.implicitly_wait(5)
driver.quit()