from retriever import *

# Do not forget to modify .env
load_dotenv()

retrieve_linkedin_profile(os.getenv("MAIL"), os.getenv("PASSWORD"), ["honors"])