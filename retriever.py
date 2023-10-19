from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pathlib
import time


def retrieve_linkedin_profile(mail, password):
    # Make (or use) a '/selenium' folder user profile to preserve session cookies
    # It's also possible to manage extensions, settings... per user basis
    options = Options()
    options.add_argument(f"user-data-dir={pathlib.Path().absolute()}\\selenium")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)

    driver.get("https://linkedin.com/")
    driver.implicitly_wait(5)

    # LinkedIn when logged in redirects to feed. If not logged, login elements should be available in main page
    if "feed" not in driver.title.lower():
        print("login required")
        driver.find_element(by=By.ID, value="session_key").send_keys(mail)
        driver.find_element(by=By.ID, value="session_password").send_keys(password, Keys.ENTER)
        driver.implicitly_wait(30) # Increase time if needed for captcha

    elif "feed" in driver.title.lower():
        print("session cookie preserved")
        
    driver.implicitly_wait(15)

    # Finds the first '/in/' href which correspond to profiles
    # This should be the one of the logged account if a clean feed page was loaded
    driver.find_element(By.XPATH, "//a[contains(@href, '/in/')]").click()
    time.sleep(20)

    # Save main profile page to HTML file for markdownification
    with open('profile_main.html', 'w', encoding="utf-8") as f:
        f.write(driver.page_source)

    driver.quit()