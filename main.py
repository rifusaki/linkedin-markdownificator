from retriever import *

# Do not forget to modify .env
load_dotenv()

login_to_profile(os.getenv("MAIL"), os.getenv("PASSWORD"))

retrieve_linkedin_profile(["honors"])