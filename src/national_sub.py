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

urlInfo = {"mc":[], "ct1":[], "ct2":[], "ct3":[], "daeClassList":[], "subContent":[], "title":[]}
urlInfoIndex=0

daeList=""
text=""

def defineCouncil(target):
    if target=="법사위": return "법제사법위원회"
    elif target=="정무위": return "정무위원회"
    elif target=="기재위": return "기획재정위원회"
    elif target=="교육위" or target=="교육위(17)": return "교육위원회"
    elif target=="과방위": return "과학기술정보방송통신위원회"
    elif target=="외통위": return "외교통일위원회"
    elif target=="국방위": return "국방위원회"
    elif target=="행안위": return "행정안전위원회"
    elif target=="문체위": return "문화체육관광위원회"
    elif target=="농해수위": return "농림축산식품해양수산위원회"
    elif target=="산자중기위": return "산업통상자원중소벤처기업위원회"
    elif target=="복지위": return "보건복지위원회"
    elif target=="환노위": return "환경노동위원회"
    elif target=="국토위": return "국토교통위원회"
    elif target=="정보위": return "정보위원회"
    elif target=="여가위": return "여성가족위원회"
    elif target=="특별위": return "특별위원회"
    elif target=="운영위": return "국회운영위원회"
    elif target=="미방위": return "미래창조과학방송통신위원회"
    elif target=="교문위": return "교육문화체육관광위원회"
    elif target=="안전행정위": return "안전행정위원회"
    elif target=="교과위": return "교육과학기술위원회"
    elif target=="외통위(19)": return "외교통상통일위원회"
    elif target=="지경위": return "지식경제위원회"
    elif target=="국토해양위": return "국토해양위원회"
    elif target=="복지가족위": return "보건복지가족위원회"
    elif target=="여성위": return "여성위원회"
    elif target=="문광위": return "문화관광위원회"
    elif target=="산자위": return "산업통상자원위원회"
    elif target=="산자위(17)": return "산업자원위원회"
    elif target=="재경위": return "재정경제위원회"
    elif target=="통외위": return "통일외교통상위원회"
    elif target=="농해위": return "농림해양수산위원회"
    elif target=="행자위": return "행정자치위원회"
    elif target=="문교공보위": return "문교공보위원회"
    elif target=="문화공보위": return "문화공보위원회"
    elif target=="외무위": return "외무통일위원회"
    elif target=="과정위": return "과학기술정보통신위원회"
    elif target=="건교위": return "건설교통위원회"
    elif target=="예결위": return "예산결산특별위원회"
    elif target=="농식품위": return "농림축산식품해양수산위원회"
    elif target=="문방위": return "문화체육관광방송통신위원회"

def purifyText(target):
    global text
    onlyCharacter=re.compile('[^a-zA-Z0-9가-힣\s%]')
    flag=False
    if target[-1]=="." or target[-1]=="?" or target[-1]=="!":
        flag=True
    if target.find("(")!=-1 and target[target.find("(")+1]!="임":
        startPoint=target.find("(")
        endPoint=target.find(")")
        newText1=target[:startPoint]
        newText2=target[endPoint:]
        target=newText1+newText2
    
    text=text+onlyCharacter.sub('',target)
    if flag: text=text+"\n"

def urlinfo(driver, contentIndex):
    global urlInfo
    global urlInfoIndex
    global daeList
    try:
        check=driver.find_element_by_css_selector("body > div.sectionBox2_03 > div > div.rightmenu > div.contenttext_box > div.doard > table > tbody > tr:nth-child("+str(contentIndex)+") > td.td_last > a > img")
        time.sleep(0.25)
        title=driver.find_element_by_css_selector("body > div.sectionBox2_03 > div > div.rightmenu > div.contenttext_box > div.doard > table > tbody > tr:nth-child("+str(contentIndex)+") > td:nth-child(1)").text.replace("-","")
        daeClassList=driver.find_element_by_css_selector("body > div.sectionBox2_03 > div > div.rightmenu > div.contenttext_box > div.doard > table > tbody > tr:nth-child("+str(contentIndex)+") > td:nth-child(5)").text
        if (daeList=="청문회" or daeList=="공청회") and len(daeClassList)>3:
            daeClassList=daeClassList[0:3]
        subContent=driver.find_element_by_css_selector("body > div.sectionBox2_03 > div > div.rightmenu > div.contenttext_box > div.doard > table > tbody > tr:nth-child("+str(contentIndex)+") > td:nth-child(3)").text
        subContent=defineCouncil(subContent)

        elem=driver.find_element_by_css_selector("body > div.sectionBox2_03 > div > div.rightmenu > div.contenttext_box > div.doard > table > tbody > tr:nth-child("+str(contentIndex)+") > td.td_last > a").get_attribute("href")
        elem=elem.split("'")
        if len(elem[3])<2:
            elem[3]="0"+elem[3]
        if len(elem[5])<3:
            while len(elem[5])<3:
                elem[5]="0"+elem[5]
        if len(elem[7])<2:
            elem[7]="0"+elem[7]

        urlInfo["mc"].append(elem[1])
        urlInfo["ct1"].append(elem[3])
        urlInfo["ct2"].append(elem[5])
        urlInfo["ct3"].append(elem[7])
        urlInfo["daeClassList"].append(daeClassList)
        urlInfo["subContent"].append(subContent)
        urlInfo["title"].append(title)

        # print("mc : "+urlInfo["mc"][urlInfoIndex])
        # print("ct1 : "+urlInfo["ct1"][urlInfoIndex])
        # print("ct2 : "+urlInfo["ct2"][urlInfoIndex])
        # print("ct3 : "+urlInfo["ct3"][urlInfoIndex])
        # print("daeClassList : "+urlInfo["daeClassList"][urlInfoIndex])
        # print("subContnet : "+urlInfo["subContent"][urlInfoIndex])
        # print("title : "+urlInfo["title"][urlInfoIndex])

        thread_down=DownText(urlInfoIndex, daeList)
        thread_down.setDaemon(True)
        thread_down.start()
        thread_down.join()

        urlInfoIndex=urlInfoIndex+1
        
        return True
    except NoSuchElementException:
        if contentIndex<=10:
            print("영상이 존재하지 않음")
        return False

def moveNumberNext(driver, numberIndex):
    contentIndex=1
    try:
        if not numberIndex==1:
            numberElem=driver.find_element_by_css_selector("body > div.sectionBox2_03 > div > div.rightmenu > div.contenttext_box > div.divPaging > div > a:nth-child("+str(numberIndex+2)+")")
            time.sleep(0.25)
            numberElem.click()
            time.sleep(0.25)

        while urlinfo(driver, contentIndex):
            contentIndex+=1

        if numberIndex%10==0:
            numberElem=driver.find_element_by_css_selector("body > div.sectionBox2_03 > div > div.rightmenu > div.contenttext_box > div.divPaging > div > a:nth-child("+str(numberIndex+3)+")")
            time.sleep(0.25)
            numberElem.click()
            time.sleep(0.25)

        return numberIndex
    except NoSuchElementException:
        return False

    

def moveSheight(driver, sheightIndex):
    numberIndex=1
    global daeList

    try:
        if not sheightIndex==1:
            sheightElem=driver.find_element_by_css_selector("#sheight > dl > dt:nth-child("+str(sheightIndex)+")")
            time.sleep(0.25)
            daeList="제"+sheightElem.text.split(" ")[0]
            sheightElem.click()
            time.sleep(0.25)
        else:
            daeList="제"+driver.find_element_by_css_selector("#sheight > dl > dt:nth-child(1) > a").text.split(" ")[0]

        lastPage=int(driver.find_element_by_xpath("//*[@title='마지막 페이지']").get_attribute("href").split("'")[1].split("'")[0])
        time.sleep(0.25)
        
        while lastPage>0:
            numberIndex=moveNumberNext(driver, numberIndex)

            if numberIndex%10==0:
                numberIndex=1
            else:
                numberIndex+=1
            lastPage-=1

        return True
    except NoSuchElementException:
        return False

def moveMenuCopy():
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument('--headless')
    firefox_options.add_argument('--no-sandbox')
    firefox_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Firefox(options=firefox_options, executable_path="./geckodriver")
    driver.get("https://w3.assembly.go.kr/vod/index.jsp")
    driver.switch_to.frame(driver.find_element_by_name("down"))

    hearingElem=driver.find_element_by_css_selector("#hederBox_01 > div.h1box_02 > ul > li:nth-child(7)")

    sheightIndex=1
    time.sleep(0.25)
    hearingElem.click()
    time.sleep(0.25)

    while moveSheight(driver, sheightIndex):
        sheightIndex+=1
        if sheightIndex==2:
            sheightIndex=3
        
    inspectElem=driver.find_element_by_css_selector("#hederBox_01 > div.h1box_02 > ul > li:nth-child(8)")
    time.sleep(0.25)
    sheightIndex=1
    inspectElem.click()
    time.sleep(0.25)

    while moveSheight(driver, sheightIndex):
        sheightIndex+=1
        if sheightIndex==2:
            sheightIndex=3
    
class DownText(threading.Thread):
    global urlInfo

    def __init__(self, urlInfoIndex, daeList):
        threading.Thread.__init__(self)
        self.urlInfoIndex=urlInfoIndex
        self.daeList=daeList

    def run(self):
        daeClassList=urlInfo["daeClassList"][self.urlInfoIndex]
        subContent=urlInfo["subContent"][self.urlInfoIndex]
        title=urlInfo["title"][self.urlInfoIndex]

        # path = url_info["mc"][ui_index]+"."+url_info["ct1"][ui_index]+"."+url_info["ct2"][ui_index]+"."+url_info["ct3"][ui_index]+"."
        if not os.path.isdir("./data/national_assembly/"+self.daeList+"/"):
            os.mkdir("./data/national_assembly/"+self.daeList+"/")
        if not os.path.isdir("./data/national_assembly/"+self.daeList+"/"+daeClassList+"/"):
            os.mkdir("./data/national_assembly/"+self.daeList+"/"+daeClassList+"/")
        if not os.path.isdir("./data/national_assembly/"+self.daeList+"/"+daeClassList+"/"+subContent+"/"):
            os.mkdir("./data/national_assembly/"+self.daeList+"/"+daeClassList+"/"+subContent+"/")
        
        if os.path.isdir("./data/national_assembly/"+self.daeList+"/"+daeClassList+"/"+subContent+"/"+title+"/"):
            print("pass ===> ./data/national_assembly/"+self.daeList+"/"+daeClassList+"/"+subContent+"/"+title+"/")
            pass
        else:
            os.mkdir("./data/national_assembly/"+self.daeList+"/"+daeClassList+"/"+subContent+"/"+title+"/")
            print("create ===> "+self.daeList+"/"+daeClassList+"/"+subContent+"/"+title+"/")
            path="./data/national_assembly/"+self.daeList+"/"+daeClassList+"/"+subContent+"/"+title+"/"

            firefox_options = webdriver.FirefoxOptions()
            firefox_options.add_argument('--headless')
            firefox_options.add_argument('--no-sandbox')
            firefox_options.add_argument('--disable-dev-shm-usage')

            url='https://w3.assembly.go.kr/jsp/vod/vod.do?cmd=vod&mc='+urlInfo["mc"][self.urlInfoIndex]+'&ct1='+urlInfo["ct1"][self.urlInfoIndex]+'&ct2='+urlInfo["ct2"][self.urlInfoIndex]+'&ct3='+urlInfo["ct3"][self.urlInfoIndex]

            driver = webdriver.Firefox(options=firefox_options, executable_path="./geckodriver")
            driver.get(url)

            textIndex=1
            global text
            try:
                while True:
                    textSub=""
                    textSub=textSub+driver.find_element_by_css_selector("#sm"+str(textIndex)).text

                    purifyText(textSub)

                    textIndex+=1
            except NoSuchElementException:
                file_path=path+title+".txt"
                Path(file_path).touch()
                text_file = open(file_path, "a")
                text_file.write(text)
                text_file.close()
                driver.quit()
            
def main():
    if not os.path.isdir('./data/'):
        os.mkdir('./data/')
    if not os.path.isdir('./data/national_assembly/'):
        os.mkdir('./data/national_assembly/')

    moveMenuCopy()

    global urlInfoIndex
    print("total text : "+str(len(urlInfo["mc"])))