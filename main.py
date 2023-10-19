from retriever import *

# Do not forget to modify .env
load_dotenv()

profile_url = login_to_profile(os.getenv("MAIL"), os.getenv("PASSWORD"))

markdownificate_profile(profile_url, ["honors"])

WebDriver.get_instance().quit()