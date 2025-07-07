from utils.retriever import *
from utils.processer import markdownify

# uncomment and indent before markdownify() to skip scraping and process local files.
#if not os.path.isfile('./data/languages.html'):
# TODO add a flag with prompt to skip or overwrite if files already exist.

# Do not forget to modify .env
load_dotenv()

profile_url = login_to_profile(os.getenv("MAIL"), os.getenv("PASSWORD"))

download_profile(profile_url, ["honors",]) # omit (do not download) details/honors/ ; not included in templates.

WebDriver.get_instance().quit()

markdownify()