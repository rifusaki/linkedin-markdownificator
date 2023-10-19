from lib import *

def start_WebDriver():
    # Make (or use) a '/selenium' folder user profile to preserve session cookies
    # It's also possible to manage extensions, settings... per user basis
    options = Options()
    options.add_argument(f"user-data-dir={Path().absolute()}\\selenium")
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=options)

class WebDriver:
    __instance__ = None

    def __init__(self):
        if WebDriver.__instance__ is not None:
            raise RuntimeError("Cannot init class twice, as it is as singelton")
        else:
            WebDriver.__instance__ = start_WebDriver()

    @classmethod
    def get_instance(cls):
        """
        :rtype: WebDriver
        """
        if cls.__instance__ is None:
            WebDriver()
        return cls.__instance__