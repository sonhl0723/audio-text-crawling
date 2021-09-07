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

textPath=""

def downloadAudio(url, group, date):
    
    wavPath="./data/tvchosun/"+group+"/"+date+"/"+date+"_full_audio.wav"

    s=requests.session()
    s.keep_alive=False
    response=s.get(url)
    html=response.text
    content=response.content
    soup=BeautifulSoup(html, 'html.parser')
    soupContent=BeautifulSoup(content, 'html.parser')

    audioUrl=str(soup).split('player_run("')[1].split('"')[0]

    title=str(soupContent).split('href="'+url+'">')[1].split("</a>")[0]

    if not os.path.isdir("./data/tvchosun/"+group+"/"+date+"/"):
        os.mkdir("./data/tvchosun/"+group+"/"+date+"/")
    if not os.path.isdir("./data/tvchosun/"+group+"/"+date+"/"+title+"/"):
        os.mkdir("./data/tvchosun/"+group+"/"+date+"/"+title+"/")
    if os.path.isfile("./data/tvchosun/"+group+"/"+date+"/"+title+"/"+title+".txt"):
        return False

    wavPath="./data/tvchosun/"+group+"/"+date+"/"+title+"/"+title+".wav"

    global textPath
    textPath="./data/tvchosun/"+group+"/"+date+"/"+title+"/"+title+".txt"

    try:
        videoClip = VideoFileClip(audioUrl)
        audioclip = videoClip.audio
        audioclip.write_audiofile(wavPath)
        audioclip.close()
        videoClip.close()
    except OSError:
        os.rmdir("./data/tvchosun/"+group+"/"+title+"/")
        print(date+" =>   No Audio")
        return False

    return True

def purifyText(target):
    resultText=""
    onlyCharacter=re.compile('[^a-zA-Z0-9가-힣\s%.]')

    for targetPiece in target:
        if targetPiece.find('[')!=-1 or targetPiece.find(']')!=-1 or targetPiece.find('/')!=-1:
                continue
        targetPiece=targetPiece.split(' ')
        for textPiece in targetPiece:
            flag=False
            # if len(textPiece)>=1:
            #     print(textPiece)
            #     print(str(ord(textPiece[0])))
            if len(textPiece)<1:
                continue
            elif textPiece[0]=='.' or textPiece[0]=='?' or textPiece[0]=='!':
                resultText=resultText+'\n'
                continue
            flag=False
            startParenthesis=textPiece.find("(")
            endParenthesis=textPiece.find(")")

            if len(textPiece)>=2:
                if textPiece[-1]=='.' and textPiece[-2].isdigit():
                    continue
                elif textPiece[-1]=='?' or textPiece[-1]=='!' or textPiece[-1]=='.':
                    textPiece=textPiece[:-1]
                    flag=True
                elif textPiece[-1]=='"' and textPiece[-2]=='.':
                    textPiece=textPiece[:-2]
                    falg=True
                
                if startParenthesis==0 and endParenthesis==len(textPiece)-1:
                    continue
                elif startParenthesis!=-1 and endParenthesis==-1:
                    textPiece=textPiece[:startParenthesis]
                elif startParenthesis==-1 and endParenthesis!=-1:
                    textPiece=textPiece[endParenthesis:]
                else:
                    newText1=textPiece[:startParenthesis]
                    newText2=textPiece[endParenthesis:]
                    textPiece=newText1+newText2
                        
            textPiece=onlyCharacter.sub('',textPiece)

            if flag:
                resultText=resultText+textPiece+'\n'
            else:
                resultText=resultText+textPiece+' '

    return resultText

def downloadText(url, group, date):
    s=requests.session()
    s.keep_alive=False
    response=s.get(url)
    # response=requests.get(url)
    if response.status_code == 200:
        html=response.content
        soup=BeautifulSoup(html.decode('utf-8', 'replace'), 'html.parser')
        wholeText=""

        checkAudio=soup.select_one("#wrap > div > div.contents > div.article_detail_body > div.vod_player")
        for i in soup.select("#wrap > div > div.contents > div.article_detail_body > div.article.font03 > p"):
            wholeText=wholeText+i.get_text()
        articleTitle=soup.select_one("#wrap > div > div.article_header > div.article_tit > h3").get_text()

        if checkAudio is None:
            print(group+" "+date+" "+articleTitle+"=>No Audio")
        elif wholeText.find(".")==-1:
            print(group+" "+date+" "+articleTitle+"=>No Text")
        elif wholeText.find("Q")!=-1:
            print(group+" "+date+" "+articleTitle+"=>Text Is Inaccurate")
        else:
            finalText=""
            wholeText=[]

            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            driver=webdriver.Chrome(options=chrome_options, executable_path="./chromedriver")
            driver.get(url)

            divNum=1
            while True:
                try:
                    elem=driver.find_element_by_css_selector("#wrap > div > div.contents > div.article_detail_body > div:nth-child("+str(divNum)+") > p")
                    time.sleep(0.25)
                    for textPiece in elem.text.split("\n"):
                        if textPiece.find(".")!=-1:
                            wholeText.append(textPiece)

                    divNum+=1
                except NoSuchElementException:
                    if divNum>5:
                        divNum=1
                        while True:
                            try:
                                elem=driver.find_element_by_css_selector("#wrap > div > div.contents > div.article_detail_body > div.article.font03 > div:nth-child("+str(divNum)+")")
                                time.sleep(0.25)
                                if elem.text is not None:
                                    for textPiece in elem.text.split("\n"):
                                        if textPiece.find(".")!=-1:
                                            wholeText.append(textPiece)

                                divNum+=1
                            except NoSuchElementException:
                                if divNum>7:
                                    break
                                else:
                                    divNum+=1
                        break
                    else:
                        divNum+=1

            finalText=finalText+purifyText(wholeText)
            if finalText=="":
                wholeText=[]
                detailNum=2
                while True:
                    try:
                        elem=driver.find_element_by_css_selector("#wrap > div > div.contents > div.article_detail_body > div:nth-child(5) > p:nth-child("+str(detailNum)+")")
                        time.sleep(0.25)
                        for textPiece in elem.text.split("\n"):
                            if textPiece.find(".")!=-1:
                                wholeText.append(textPiece)

                        detailNum+=1
                    except NoSuchElementException:
                        break
                finalText=finalText+purifyText(wholeText)

            driver.delete_all_cookies()
            driver.quit()

            global textPath
            # file_path = "./data/tvchosun/"+str(i)+"/"+year+month+day+"/"+year+month+day+"_full_text.txt"
            # file_path=textPath
            Path(textPath).touch()
            text_file = open(textPath, "a")
            text_file.write(finalText)
            text_file.close()
    else:
        print(response.status_code)

def collectTextUrl(url):
    pageNum=1
    contentNum=1
    textUrl=[]
    lastFlag=0

    while True:
        detailedUrl=url+"&pn="+str(pageNum)
        s=requests.session()
        s.keep_alive=False
        response=s.get(detailedUrl)
        # response=requests.get(detailedUrl)
        html=response.text
        soup=BeautifulSoup(html, 'html.parser')

        for i in soup.select('#iframe > div.bbs_zine.top_line > ul > li > div.detail > p.article_tit > a'):
            elem=i.get("onclick").split("'")[1].split("'")[0]
            if not elem.find("vir")!=-1:
                textUrl.append(elem)

        pageNum+=1
        detailedUrl=url+"&pn="+str(pageNum)
        if wrongDateCheck(detailedUrl):
            break

    return textUrl

def wrongDateCheck(url):
    s=requests.session()
    s.keep_alive=False
    response=s.get(url)
    # response=requests.get(url)
    if response.status_code == 200:
        html=response.text
        soup=BeautifulSoup(html, 'html.parser')

        try:
            checkItem=soup.select_one("#iframe > div.popular_tag.mgt40 > h3").get_text()

            return True
        except AttributeError as e:
            return False
    else:
        print(response.status_code)
        return True

def main():
    if not os.path.isdir('./data/'):
        os.mkdir('./data/')
    if not os.path.isdir('./data/tvchosun/'):
        os.mkdir('./data/tvchosun/')

    news9={"url":"http://broadcast.tvchosun.com/news/newspan/ch19.cstv", "dateList":[]}
    lastDate={"news9":["2013","03","04"]}

    for i in lastDate:
        if not os.path.isdir("./data/tvchosun/"+str(i)+"/"):
            os.mkdir("./data/tvchosun/"+str(i)+"/")
        lastYear=lastDate[i][0]
        lastMonth=lastDate[i][1]
        lastDay=lastDate[i][2]

        year="2016"
        month="05"
        day="24"

        baseUrl="http://news.tvchosun.com/svc/vod/ospc_news_prog_pan.html?catid=2P&replay_full_new.html?catid=2P&indate="

        checkTotal=0
        checkWrong=0

        while True:
            url=baseUrl+year+month+day
            audioDownFlag=True

            if not wrongDateCheck(url):
                textUrlList=collectTextUrl(url)
                textUrlList=textUrlList[1:]

                for textUrl in textUrlList:
                    if downloadAudio(textUrl, str(i), year+month+day):
                        downloadText(textUrl, str(i), year+month+day)

                    checkTotal+=1
                else:
                    print("Already Downloaded")
            else:
                checkWrong+=1
            if day=="01":
                day="31"
                month=str(int(month)-1)

                if month=="0":
                    month="12"
                    year=str(int(year)-1)
                elif len(month)==1:
                    month="0"+month
            else:
                day=str(int(day)-1)
                if len(day)==1:
                    day="0"+day

            if int(year+month+day)<int(lastYear+lastMonth+lastDay):
                print(i+" checkTotal:"+str(checkTotal))
                break