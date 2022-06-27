from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
import os
import time
import threading
from pathlib import Path
import re

base_path = "./data/national_assembly/"

conf_data =\
    {
        "MAIN_COUNCIL_URL": "http://likms.assembly.go.kr/record/mhs-40-010.do",
        "TEXT_BASE_URL": "https://w3.assembly.go.kr/jsp/vod/vod.do?cmd=vod&mc=",
        "MAIN_PAGE": "https://w3.assembly.go.kr/vod/index.jsp",
    }

webdriver_option = ['--headless', '--no-sandbox', '--disable-dev-shm-usage']

webdriver_profile = ["browser.cache.disk.enable", "browser.cache.memory.enable", "browser.cache.offline.enable", "network.http.use-cache"]