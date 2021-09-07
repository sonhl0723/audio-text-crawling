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

from lxml import html
from xml.sax import saxutils as su

finalText=""
totalCheck=0

def purifyText(target):
    resultText=""
    onlyCharacter=re.compile('[^a-zA-Z0-9가-힣\s%.]')

    for targetPiece in target:
        if targetPiece[0]=='\n':
            continue
        elif targetPiece[0]=="[" and targetPiece.find(".")==-1:
            continue
        elif len(targetPiece)>1 and targetPiece[0].isdigit() and targetPiece[1]==".":
            continue

        if targetPiece[0]=="[" and targetPiece.find(".")!=-1 and targetPiece.find(":")!=-1:
            targetPiece=targetPiece.split(":")[1]
            targetPiece=targetPiece[:-1]

        targetPiece=re.sub(r'\([^)]*\)', '', targetPiece)
        index=targetPiece.find(".")
        if index==-1:
            resultText=resultText+targetPiece
        while index > -1:
            try:
                if index!=0 and index!=len(targetPiece):
                    if not targetPiece[index-1].isdigit():
                        resultText=resultText+targetPiece[:index]+'\n'
                        targetPiece=targetPiece[index+1:]
                    else:
                        resultText=resultText+targetPiece[:index+1]
                        targetPiece=targetPiece[index+2:]
                elif index==len(targetPiece):
                    resultText=result+targetPiece[:-1]+'\n'
                    targetPiece=""
                elif index==0:
                    targetPiece=targetPiece[1:]

                index=targetPiece.find(".")
            except ValueError:
                break

    return resultText

def downloadAudio(url, path):
    response=requests.get(url)
    html=response.text
    soup=BeautifulSoup(html, 'html.parser')
    cssSelector=str(soup).split("_contents_s@")[1].split('id="')[1].split('"')[0].split('_')[1]

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver=webdriver.Chrome(options=chrome_options, executable_path="./chromedriver")

    # --------------------------------------------------test
    # firefox_options = webdriver.FirefoxOptions()
    # firefox_options.add_argument('--headless')
    # firefox_options.add_argument('--no-sandbox')
    # firefox_options.add_argument('--disable-dev-shm-usage')
    # driver=webdriver.Firefox(options=firefox_options, executable_path="./geckodriver")
    # --------------------------------------------------test

    driver.get(url)
    elem=driver.find_element_by_css_selector("#"+cssSelector+"-id")
    time.sleep(0.25)
    audioUrl=elem.get_attribute("src")
    driver.quit()

    videoClip=VideoFileClip(audioUrl)
    audioclip=videoClip.audio
    audioclip.write_audiofile(path)
    audioclip.close()
    videoClip.close()

def downloadText(videoUrl, title):
    titleIndex=0
    text=""
    global finalText

    for url in videoUrl:
        if not os.path.isdir('./data/jtbc/newsRoom/'+title[titleIndex]):
            os.mkdir('./data/jtbc/newsRoom/'+title[titleIndex])
        # if os.path.isfile("./data/jtbc/newsRoom/"+title[titleIndex]+"/"+title[titleIndex]+"_full_text.txt") and os.path.isfile("./data/jtbc/newsRoom/"+title[titleIndex]+"/"+title[titleIndex]+"_full_audio.wav"):
        #     print("Already Downloaded => "+title[titleIndex])
        #     titleIndex+=1
        #     continue

        # ---------------test
        if os.path.isfile("./data/jtbc/newsRoom/"+title[titleIndex]+"/"+title[titleIndex]+"_full_text.txt"):
            print("Already Downloaded => "+title[titleIndex])
            titleIndex+=1
            continue

        finalText=""
        response = requests.get(url)
        s=response.text
        soup=BeautifulSoup(s, 'html.parser')
        textUrl=[i['href'] for i in soup.select('#articlebody > div:nth-child(2) > div.article_list_wrap > div > div.bd > a')]

        for textComponent in textUrl:
            # print(textComponent) #test
            textResponse=requests.get(textComponent)
            tree=html.fromstring(textResponse.content)
            fullText=tree.xpath("//*[@id='articlebody']/div[1]/text()")
            
            finalText+=purifyText(fullText)
            

        onlyCharacter=re.compile('[^a-zA-Z0-9가-힣\s%.]')
        changeLine = finalText.maketrans("?!", "\n\n")
        finalText=finalText.translate(changeLine)
        finalText=onlyCharacter.sub('', finalText)
        finalText=finalText.replace(u'\xa0', u' ')

        file_path = "./data/jtbc/newsRoom/"+title[titleIndex]+"/"+title[titleIndex]+"_full_text.txt"
        if os.path.isfile(file_path):
            os.remove(file_path)
        Path(file_path).touch()
        text_file = open(file_path, "a")
        text_file.write(finalText)
        text_file.close()

        # downloadAudio(url, "./data/jtbc/newsRoom/"+title[titleIndex]+"/"+title[titleIndex]+"_full_audio.wav")

        print("Download Success => "+title[titleIndex])
        global totalCheck
        totalCheck+=1

        titleIndex+=1
        

def currentDateCheck():
    response = requests.get("https://news.jtbc.joins.com/Replay/news_replay.aspx?fcode=PR10000403")
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    return soup.select_one("#form1 > div.news_main > div.review_list > div.hd > h4").text.split(" ")[0].replace(".","")

def main():
    if not os.path.isdir('./data/'):
        os.mkdir('./data/')
    if not os.path.isdir('./data/jtbc/'):
        os.mkdir('./data/jtbc/')
    if not os.path.isdir('./data/jtbc/newsRoom/'):
        os.mkdir('./data/jtbc/newsRoom/')

    date=currentDateCheck()
    year=date[0:4]
    month=date[4:6]
    day=date[6:]
    #---test
    # year="2021"
    # month="01"
    # day="19"
    # date=year+month+day

    baseUrl="https://news.jtbc.joins.com/Replay/news_replay.aspx?fcode=PR10000403&strSearchDate="
    title=[]
    lastYear="2015"
    lastMonth="01"
    lastDay="02"

    while True:
        url=baseUrl+date

        global totalCheck
        if totalCheck%30==0:
            time.sleep(0.25)

        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        videoUrl=[]
        video = [i['href'] for i in soup.select('#form1 > div.news_main > div.review_list > div.bd > ul > li > div.lt > a')]
        if str(soup).find("1부")==-1:
            try:
                videoUrl.append(video[0])
            except IndexError:
                videoUrl.append(video[0])
        else:
            videoUrl=video[0:2]

        if len(videoUrl)>1:
            title.append(date+"_1")
            title.append(date+"_2")
            if not os.path.isdir('./data/jtbc/newsRoom/'+title[0]):
                os.mkdir('./data/jtbc/newsRoom/'+title[0])
            if not os.path.isdir('./data/jtbc/newsRoom/'+title[1]):
                os.mkdir('./data/jtbc/newsRoom/'+title[1])
        else:
            title.append(date)
            if not os.path.isdir('./data/jtbc/newsRoom/'+title[0]):
              os.mkdir('./data/jtbc/newsRoom/'+title[0])

        downloadText(videoUrl, title)

        videoUrl.clear()
        title.clear()

        if day=="01":
            month=str(int(month)-1)

            if month=="0":
                month="12"
                year=str(int(year)-1)
            elif len(month)==1:
                month="0"+month

            if month=="04" or month=="06" or month=="09" or month=="11":
                day="30"
            elif month=="02":
                day="28"
            else:
                day="31"

        else:
            day=str(int(day)-1)
            if len(day)==1:
                day="0"+day

        if int(year+month+day)<int(lastYear+lastMonth+lastDay):
            print("total: "+str(totalCheck))
            print("lastDate: "+date)
            break

        date=year+month+day

main()

# response = requests.get("https://news.jtbc.joins.com/article/article.aspx?news_id=NB11902858")
# tree=html.fromstring(response.content)
# text=tree.xpath("//*[@id='articlebody']/div[1]/text()")
# print(text)
# print(purifyText(text))
# purifyText(text)