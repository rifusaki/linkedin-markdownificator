from utils.lib import *
from utils.driver import *


def login_to_profile(mail, password):
    driver = WebDriver.get_instance()
    driver.get("https://linkedin.com/login")
    driver.implicitly_wait(15)

    if "feed" not in driver.title.lower():
        print("login required")
        for el in driver.find_elements(By.CSS_SELECTOR, 'input[autocomplete="username"]'):
            if el.is_displayed():
                el.send_keys(mail)
                break
        for el in driver.find_elements(By.CSS_SELECTOR, 'input[autocomplete="current-password"]'):
            if el.is_displayed():
                el.send_keys(password, Keys.ENTER)
                break
        print("Post-login: waiting up to 60s for CAPTCHA/2FA verification...")
        print("  (solve any challenge in the browser window)")
        for remaining in range(60, 0, -5):
            time.sleep(5)
            if "feed" in driver.title.lower():
                print("Feed loaded.")
                break
            print(f"  still waiting... ({remaining}s)")
        print(f"  Final URL: {driver.current_url}")

    print("Navigating to profile...")
    driver.find_element(By.XPATH, "//a[contains(@href, '/in/')]").click()
    time.sleep(5)

    return driver.current_url


# The following dictionary contains the pages to be retrieved.
retrieval = ("main", "featured", "experience", "education", "certifications", "projects", "honors", "courses", "languages")

# Omit argument excludes pages from previous tuple
def download_profile(profile_url, omit = []):
    driver = WebDriver.get_instance()

    to_retrieve = [i for i in list(retrieval) if i not in omit]
    for element in to_retrieve:
        os.makedirs(os.path.dirname(f"data/{element}.html"), exist_ok=True)
        element_file = open(f"data/{element}.html", "w", encoding="utf-8")
        if element != "main":   
            driver.get(profile_url+f"details/{element}/")
            time.sleep(3)
        element_file.write(driver.page_source)
        element_file.write("\n")
        element_file.close()