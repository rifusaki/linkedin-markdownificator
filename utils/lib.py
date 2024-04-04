from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
from parsel import Selector
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from builtins import zip, len
import time
import os