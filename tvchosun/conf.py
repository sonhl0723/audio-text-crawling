import requests
from bs4 import BeautifulSoup
import os
from pathlib import Path
import re
from moviepy.editor import *
import os
from pathlib import Path

from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException


conf_data =\
    {
        "LAST_DATE": {"news9":["2016","05","25"], "news7":["2017","07","08"]},
        "NEWS7_URL": ["http://news.tvchosun.com/svc/vod/ospc_news_prog_pan.html?catid=75&replay_full_new.html?catid=75&indate=","http://news.tvchosun.com/svc/vod/replay_full_new.html?catid=75&indate="],
        "NEWS9_URL": ["http://news.tvchosun.com/svc/vod/ospc_news_prog_pan.html?catid=2P&replay_full_new.html?catid=2P&indate=","http://news.tvchosun.com/svc/vod/replay_full_new.html?catid=2P&indate="],
    }

base_path = "./data/tvchosun/"

webdriver_option = ['--headless', '--no-sandbox', '--disable-dev-shm-usage']