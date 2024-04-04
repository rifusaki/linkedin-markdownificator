from utils.retriever import *
from utils.processer import markdownify

# Do not forget to modify .env
load_dotenv()

profile_url = login_to_profile(os.getenv("MAIL"), os.getenv("PASSWORD"))

download_profile(profile_url, ["honors", "certifications", "education", "experience", "featured", "languages", "main", "projects", "skills"])

WebDriver.get_instance().quit()

# markdownify()