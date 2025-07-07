from utils.retriever import *
from utils.processer import markdownify

if not os.path.isfile('./data/languages.html'):
  # Do not forget to modify .env
  load_dotenv()

  profile_url = login_to_profile(os.getenv("MAIL"), os.getenv("PASSWORD"))

  download_profile(profile_url, ["honors",])

  WebDriver.get_instance().quit()

markdownify()