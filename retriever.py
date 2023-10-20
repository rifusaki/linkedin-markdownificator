from lib import *
from driver import *


def login_to_profile(mail, password):
    driver = WebDriver.get_instance()
    driver.get("https://linkedin.com/")
    driver.implicitly_wait(10)

    # LinkedIn when logged in redirects to feed. If not logged, login elements should be available in main page
    if "feed" not in driver.title.lower():
        print("login required")
        driver.find_element(by=By.ID, value="session_key").send_keys(mail)
        driver.find_element(by=By.ID, value="session_password").send_keys(password, Keys.ENTER)
        driver.implicitly_wait(30) # Increase time if needed for captcha

    # Finds the first '/in/' href which correspond to profiles
    # This should be the one of the logged account if a clean feed page was loaded
    driver.find_element(By.XPATH, "//a[contains(@href, '/in/')]").click()

    return driver.current_url


# The following dictionary contains the pages to be retrieved along with the XPATH expression to select relevant information
retrieval = {"main": ("//*[@class='text-heading-xlarge inline t-24 v-align-middle break-words']",
                      "//div[@class='text-body-medium break-words']",
                      "//div[@data-generated-suggestion-target='urn:li:fsu_profileActionDelegate:-1983837190']",
                      "//div[@class='pvs-media-content__preview']",
                      "//div[@class='pvs-media-content__image-wrapper']"), 
             "experience": ("",), 
             "education": ("",), 
             "certifications": ("",), 
             "projects": ("",),
             "skills": ("",), 
             "honors": ("",), 
             "languages": ("",)}


def markdownificate_profile(profile_url, omit = []):
    driver = WebDriver.get_instance()
    profile = open("profile.txt", "w", encoding="utf-8")

    to_retrieve = [i for i in list(retrieval.keys()) if i not in omit]
    for element in to_retrieve:
        driver.get(profile_url+f"details/{element}/")
        time.sleep(3)
        retrieve_information(element, profile)
    
    profile.close()

def retrieve_information(key, file):
    driver = WebDriver.get_instance()

    for expression in retrieval[key]:
        if expression != "":
            elements = [i.text for i in driver.find_elements(By.XPATH, expression)]
            for element in elements:
                file.write(element + "\n")
            file.write("\n")
