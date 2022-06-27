from jtbc.conf import *
from jtbc.utils import prep_text

def download_audio(url, path):
    response=requests.get(url)
    html=response.text
    soup=BeautifulSoup(html, 'html.parser')
    css_selector=str(soup).split("_contents_s@")[1].split('id="')[1].split('"')[0].split('_')[1]

    # --------------------------------------------------chrome
    chrome_options = webdriver.ChromeOptions()
    for option in webdriver_option: chrome_options.add_argument(option)
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    driver=webdriver.Chrome(options=chrome_options, executable_path="./chromedriver")
    # --------------------------------------------------chrome

    # --------------------------------------------------firefox
    # firefox_options = webdriver.FirefoxOptions()
    # for option in webdriver_option: firefox_options.add_argument(option)
    # # firefox_options.add_argument('--headless')
    # # firefox_options.add_argument('--no-sandbox')
    # # firefox_options.add_argument('--disable-dev-shm-usage')
    # driver=webdriver.Firefox(options=firefox_options, executable_path="./geckodriver")
    # --------------------------------------------------firefox

    driver.get(url)
    elem=driver.find_element_by_css_selector("#"+css_selector+"-id")
    time.sleep(0.25)
    audio_url=elem.get_attribute("src")
    driver.quit()

    video_clip=VideoFileClip(audio_url)
    audio_clip=video_clip.audio
    audio_clip.write_audiofile(path)
    audio_clip.close()
    video_clip.close()

def download_text(videoUrl, title):
    title_idx=0

    for url in videoUrl:
        if not os.path.isdir('./data/jtbc/newsRoom/'+title[title_idx]):
            os.mkdir('./data/jtbc/newsRoom/'+title[title_idx])
        if os.path.isfile("./data/jtbc/newsRoom/"+title[title_idx]+"/"+title[title_idx]+"_full_text.txt"):
            print("Already Downloaded => "+title[title_idx])
            title_idx+=1
            continue

        final_text=""
        response = requests.get(url)
        s=response.text
        soup=BeautifulSoup(s, 'html.parser')
        text_url=[i['href'] for i in soup.select('#articlebody > div:nth-child(2) > div.article_list_wrap > div > div.bd > a')]

        for comp in text_url:
            textResponse=requests.get(comp)
            tree=html.fromstring(textResponse.content)
            full_text=tree.xpath("//*[@id='articlebody']/div[1]/text()")
            
            final_text+=prep_text(full_text)
            
        only_character=re.compile('[^a-zA-Z0-9가-힣\s%.]')
        change_line = final_text.maketrans("?!", "\n\n")
        final_text=final_text.translate(change_line)
        final_text=only_character.sub('', final_text)
        final_text=final_text.replace(u'\xa0', u' ')

        file_path = "./data/jtbc/newsRoom/"+title[title_idx]+"/"+title[title_idx]+"_full_text.txt"
        if os.path.isfile(file_path):
            os.remove(file_path)
        Path(file_path).touch()
        text_file = open(file_path, "a")
        text_file.write(final_text)
        text_file.close()

        download_audio(url, "./data/jtbc/newsRoom/"+title[title_idx]+"/"+title[title_idx]+"_full_audio.wav")

        print("Download Success => "+title[title_idx])

        title_idx+=1

    return True