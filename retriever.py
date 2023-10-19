from lib import *

def retrieve_linkedin_profile(mail, password, omit = []):
    # Make (or use) a '/selenium' folder user profile to preserve session cookies
    # It's also possible to manage extensions, settings... per user basis
    options = Options()
    options.add_argument(f"user-data-dir={Path().absolute()}\\selenium")
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
        
    driver.implicitly_wait(15)

    # Finds the first '/in/' href which correspond to profiles
    # This should be the one of the logged account if a clean feed page was loaded
    driver.find_element(By.XPATH, "//a[contains(@href, '/in/')]").click()
    time.sleep(5)
    profile_url = driver.current_url

    # Save main profile and detail pages to HTML files for markdownification
    Path("html_profile/").mkdir(parents=True, exist_ok=True)

    with open('html_profile/profile_main.html', 'w', encoding="utf-8") as f:
        f.write(driver.page_source)
    
    to_retrieve = [i for i in ["experience", "education", "certifications", "projects",
                   "skills", "honors", "languages"] if i not in omit]
    
    for element in to_retrieve:
        driver.get(profile_url+f"details/{element}/")
        time.sleep(5)
        with open(f'html_profile/{element}.html', 'w', encoding="utf-8") as f:
            f.write(driver.page_source)

    driver.quit()