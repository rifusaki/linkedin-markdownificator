from utils.lib import *
from utils.driver import *


def login_to_profile(mail, password):
    driver = WebDriver.get_instance()
    driver.get("https://linkedin.com/login")
    driver.implicitly_wait(15)

    # LinkedIn when logged in redirects to feed. If not logged, login elements should be available in main page
    if "feed" not in driver.title.lower():
        print("login required")
        #driver.find_element(by=By.ID, value="session_key").send_keys(mail)
        driver.find_element(by=By.ID, value="username").send_keys(mail)
        #driver.find_element(by=By.ID, value="session_password").send_keys(password, Keys.ENTER)
        driver.find_element(by=By.ID, value="password").send_keys(password, Keys.ENTER)
        driver.implicitly_wait(30) # Increase time if needed for captcha

    # Finds the first '/in/' href which correspond to profiles
    # This should be the one of the logged account if a clean feed page was loaded
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