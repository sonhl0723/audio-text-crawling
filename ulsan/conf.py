import os
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

import requests
from bs4 import BeautifulSoup
from pathlib import Path
import re
from moviepy.editor import *

text_page_list = [5, 5, 5, 5, 5, 5, 7, 7, 7, 7, 7]

# 다운로드 받지 않을 시작 href
break_href_list = ['/cast/viewVod.do?vod=732&bt=E',
'/cast/viewVod.do?vod=1087&bt=E',
'/cast/viewVod.do?vod=1096&bt=E',
'/cast/viewVod.do?vod=1094&bt=E',
'/cast/viewVod.do?vod=1098&bt=E']

# 다운받을 마지막 날짜
last_date_list = ['20100715', '20110210', '20110210', '20110210', '20110210', '20110511', '20181210', '20200826', '20200910', '20190718', '20210312']

# 회의록 범위
text_range_list = [[129, 221], [134, 221], [134, 221], [134, 221], [134, 221], [137, 220], [201, 213], [215, 220], [216, 217], [206, 218], [220, 221]]

text_url_change = ['C101', 'C601', 'C701', 'C501', 'C801', 'E011', 'E014', 'E017', 'E018', 'E015', 'E019']

mkdir_list = ['council_operation', 'administration', 'environment', 'industry', 'education', 'budget', 'energy', 'young', 'economy', 'confirmation', 'nuclear']

base_url = 'https://www.council.ulsan.kr/minutes/assembly/search/simple1.html?daesu='

select_council_url = 'http://www.council.ulsan.kr/cast/sub/list.do?bbsId=castActivityVod&commCode='

base_path = '../data/ulsan/'