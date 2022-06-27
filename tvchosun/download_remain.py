from tvchosun.conf import *
from tvchosun.utils import prep_text

text_path = ""

def download_audio(url, group, date):
    
    wav_path=base_path+group+"/"+date+"/"+date+"_full_audio.wav"

    s=requests.session()
    s.keep_alive=False
    response=s.get(url)
    html=response.text
    content=response.content
    soup=BeautifulSoup(html, 'html.parser')
    soup_content=BeautifulSoup(content, 'html.parser')

    audio_url=str(soup).split('player_run("')[1].split('"')[0]

    title=str(soup_content).split('href="'+url+'">')[1].split("</a>")[0]

    if not os.path.isdir(base_path+group+"/"+date+"/"): os.mkdir(base_path+group+"/"+date+"/")
    if not os.path.isdir(base_path+group+"/"+date+"/"+title+"/"): os.mkdir(base_path+group+"/"+date+"/"+title+"/")
    if os.path.isfile(base_path+group+"/"+date+"/"+title+"/"+title+".txt"): return False

    wav_path=base_path+group+"/"+date+"/"+title+"/"+title+".wav"

    global text_path
    text_path=base_path+group+"/"+date+"/"+title+"/"+title+".txt"

    try:
        videoClip = VideoFileClip(audio_url)
        audioclip = videoClip.audio
        audioclip.write_audiofile(wav_path)
        audioclip.close()
        videoClip.close()
    except OSError:
        os.rmdir(base_path+group+"/"+title+"/")
        print(date+" =>   No Audio")
        return False

    return True

def download_text(url, group, date):
    s=requests.session()
    s.keep_alive=False
    response=s.get(url)

    if response.status_code == 200:
        html=response.content
        soup=BeautifulSoup(html.decode('utf-8', 'replace'), 'html.parser')
        whole_text=""

        check_audio=soup.select_one("#wrap > div > div.contents > div.article_detail_body > div.vod_player")
        for i in soup.select("#wrap > div > div.contents > div.article_detail_body > div.article.font03 > p"): whole_text=whole_text+i.get_text()
        article_title=soup.select_one("#wrap > div > div.article_header > div.article_tit > h3").get_text()

        if check_audio is None: print(group+" "+date+" "+article_title+"=>No Audio")
        elif whole_text.find(".")==-1: print(group+" "+date+" "+article_title+"=>No Text")
        elif whole_text.find("Q")!=-1: print(group+" "+date+" "+article_title+"=>Text Is Inaccurate")
        else:
            final_text=""
            whole_text=[]

            # --------------------------------------------------firefox
            firefox_options = webdriver.FirefoxOptions()
            for option in webdriver_option: firefox_options.add_argument(option)
            driver=webdriver.Firefox(options=firefox_options, executable_path="./geckodriver")
            # --------------------------------------------------firefox
            driver.get(url)

            div_num=1
            while True:
                try:
                    elem=driver.find_element_by_css_selector("#wrap > div > div.contents > div.article_detail_body > div:nth-child("+str(div_num)+") > p")
                    time.sleep(0.25)
                    for sent in elem.text.split("\n"):
                        if sent.find(".")!=-1:
                            whole_text.append(sent)

                    div_num+=1
                except NoSuchElementException:
                    if div_num>5:
                        div_num=1
                        while True:
                            try:
                                elem=driver.find_element_by_css_selector("#wrap > div > div.contents > div.article_detail_body > div.article.font03 > div:nth-child("+str(div_num)+")")
                                time.sleep(0.25)
                                if elem.text is not None:
                                    for sent in elem.text.split("\n"):
                                        if sent.find(".")!=-1: whole_text.append(sent)

                                div_num+=1
                            except NoSuchElementException:
                                if div_num>7: break
                                else: div_num+=1
                        break
                    else: div_num+=1

            final_text=final_text+prep_text(whole_text)
            if final_text=="":
                whole_text=[]
                detailNum=2
                while True:
                    try:
                        elem=driver.find_element_by_css_selector("#wrap > div > div.contents > div.article_detail_body > div:nth-child(5) > p:nth-child("+str(detailNum)+")")
                        time.sleep(0.25)
                        for sent in elem.text.split("\n"):
                            if sent.find(".")!=-1: whole_text.append(sent)

                        detailNum+=1
                    except NoSuchElementException: break
                final_text=final_text+prep_text(whole_text)

            driver.delete_all_cookies()
            driver.quit()

            global text_path
            Path(text_path).touch()
            text_file = open(text_path, "a")
            text_file.write(final_text)
            text_file.close()
    else: print(response.status_code)