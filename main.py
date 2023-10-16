from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import os

load_dotenv()
driver = webdriver.Chrome()

driver.get("https://co.linkedin.com/")
driver.implicitly_wait(2)

driver.find_element(by=By.ID, value="session_key").send_keys(os.getenv("MAIL"))
password = driver.find_element(by=By.ID, value="session_password")
password.send_keys(os.getenv("PASSWORD"), Keys.ENTER)
driver.implicitly_wait(30)

driver.quit()