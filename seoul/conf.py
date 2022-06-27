import requests
from bs4 import BeautifulSoup
import os
from pathlib import Path
import re
from moviepy.editor import *

url_change = ["A", "C010", "C030", "C050", "C130", "C163", "C165", "C207", "C191", "C200", "C210", "E", "G"]

last_date_list = {"A" : "20031219", "C010" : "20140724(3)", "C030" : "20140724", "C050" : "20140724", "C130" : "20140925", "C163" : "20140925",
"C165" : "20140922", "C207" : "20140924", "C191" : "20140718", "C200" : "20140828", "C210" : "20140925", "E" : "20140929", "G" : "20180917"}

mkdir_list = {"A" : "real", "C010" : "operation", "C030" : "administration", "C050" : "economy", "C130" : "environment", "C163" : "physical",
"C165" : "sanitation", "C207" : "safe", "C191" : "plan", "C200" : "traffic", "C210" : "edu", "E" : "budget", "G" : "special"}

base_url = "./data/seoul/"