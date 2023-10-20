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
retrieval = {"main": (("h1", {"class_" : "text-heading-xlarge inline t-24 v-align-middle break-words"}),
                      ("div", {"class_" : "text-body-medium break-words"}),
                      ("span", {"class_" : "text-body-small inline t-black--light break-words"})),
             "featured" : (("div", {"class_" : "artdeco-card full-width overflow-hidden display-flex flex-column"}),), 
             "experience": (("div", {"data-view-name" : "profile-component-entity"}),), 
             "education": (("div", {"data-view-name" : "profile-component-entity"}),), 
             "certifications": (("div", {"data-view-name" : "profile-component-entity"}),), 
             "projects": (("div", {"data-view-name" : "profile-component-entity"}),),
             "skills": (("div", {"data-view-name" : "profile-component-entity"}),), 
             "honors": ("",), # Pending
             "languages": (("div", {"data-view-name" : "profile-component-entity"}),)}


def markdownificate_profile(profile_url, omit = []):
    driver = WebDriver.get_instance()
    profile = open("profile2.txt", "w", encoding="utf-8")

    # retrieve_information(driver.page_source, profile)

    to_retrieve = [i for i in list(retrieval.keys()) if i not in omit]
    for element in to_retrieve:
        if element != "main":   
            driver.get(profile_url+f"details/{element}/")
            time.sleep(3)
        retrieve_information(element, driver.page_source, profile)
        profile.write("\n")
    
    profile.close()

def retrieve_information(key, page_source, file):
    driver = WebDriver.get_instance()

    soup = bs(page_source, "html.parser")

    for expression in retrieval[key]:
        if expression != "":
            file.write(str(soup.find_all(expression[0], **expression[1]))+"\n")
