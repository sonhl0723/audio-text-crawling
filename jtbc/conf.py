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


conf_data =\
    {
        "CURRENT_URL": "https://news.jtbc.joins.com/Replay/news_replay.aspx?fcode=PR10000403",
    }

webdriver_option = ['--headless', '--no-sandbox', '--disable-dev-shm-usage']

last_date = ["2015", "01", "02"]

base_path = "./data/jtbc/"

final_path = base_path+"newsRoom/"