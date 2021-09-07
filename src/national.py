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

url_info = {"mc":[], "ct1":[], "ct2":[], "ct3":[]}
urlinfo_index=0
testCheck=0

lock=threading.Lock()

def purifyText(target):
    onlyCharacter=re.compile('[^a-zA-Z0-9가-힣\s%]')
    flag=False
    if len(target)>1:
        if target[-1]=="." or target[-1]=="?" or target[-1]=="!":
            flag=True
    if target.find("(")!=-1 and target.find("(")!=(len(target)-1):
        if target[target.find("(")+1]!="임":
            startPoint=target.find("(")
            endPoint=target.find(")")
            newText1=target[:startPoint]
            newText2=target[endPoint:]
            target=newText1+newText2
        
    target=onlyCharacter.sub('',target)
    if flag: target=target+"\n"

    return target

def check_confirmCommMenu(driver, page_flag):
    if page_flag:
        try:
            # elem=driver.find_element_by_xpath("//*[@id='confirmCommMenu']")
            elem=driver.find_element_by_css_selector("#confirmCommMenu")
            time.sleep(0.25)
            elem.click()
            time.sleep(0.25)
            return True
        except NoSuchElementException:
            return False
    else:
        try:
            # elem=driver.find_element_by_xpath("//*[@id='confirmCommMenu']")
            elem=driver.find_element_by_css_selector("#confirmCommMenu")
            time.sleep(0.25)
            elem.click()
            time.sleep(0.25)
            return True
        except ElementNotInteractableException or NoSuchElementException:
            return False

# def check_subCommMenu(driver, page_flag):
#     if page_flag:
#         try:
#             # elem=driver.find_element_by_xpath("//*[@id='subCommMenu']")
#             elem=driver.find_element_by_css_selector("#subCommMenu")
#             time.sleep(0.25)
#             elem.click()
#             time.sleep(0.25)
#             return True
#         except NoSuchElementException:
#             return False
#     else:
#         try:
#             # elem=driver.find_element_by_xpath("//*[@id='subCommMenu']")
#             elem=driver.find_element_by_css_selector("#subCommMenu")
#             time.sleep(0.25)
#             elem.click()
#             time.sleep(0.25)
#             return True
#         except ElementNotInteractableException or NoSuchElementException:
#             return False

def check_publicCommMenu(driver, page_flag):
    try:
        # elem=driver.find_element_by_xpath("//*[@id='publicCommMenu']")
        elem=driver.find_element_by_css_selector("#publicCommMenu")
        time.sleep(0.25)
        elem.click()
        time.sleep(0.25)
        return True
    except ElementNotInteractableException or NoSuchElementException:
        return False

def check_hearingCommMenu(driver, page_flag):
    if page_flag:
        try:
            # elem=driver.find_element_by_xpath("//*[@id='hearingCommMenu']")
            elem=driver.find_element_by_css_selector("#hearingCommMenu")
            time.sleep(0.25)
            elem.click()
            time.sleep(0.25)
            return True
        except ElementNotInteractableException or NoSuchElementException:
            return False
    else:
        try:
            # elem=driver.find_element_by_xpath("//*[@id='hearingCommMenu']")
            elem=driver.find_element_by_css_selector("#hearingCommMenu")
            time.sleep(0.25)
            elem.click()
            time.sleep(0.25)
            return True
        except ElementNotInteractableException or NoSuchElementException:
            return False

def check_ctonly(driver, mainct_num, subct_num, sub_flag):
    if sub_flag==0: # sub button이 없는 경우
        try:
            # driver.find_element_by_xpath("//*[@id='content']/div/ul/li["+str(mainct_num)+"]/div[2]/div/ul/li/span/span/a[3]")
            driver.find_element_by_css_selector("#content > div > ul > li.minutes_open > div.open_wrap02 > div > ul > li > span > span > a:nth-child(3)")
            time.sleep(0.25)

            return 1 #sub button 없고 항목 하나 있는 경우
        except NoSuchElementException:
            try:
                driver.find_element_by_css_selector("#content > div > ul > li.minutes_open > div.open_wrap02 > div > ul > li:nth-child(1) > span > span > a:nth-child(3)")
                time.sleep(0.25)
                return 2 #sub button 없고 항목 여러개 있는 경우
            except NoSuchElementException:
                return False

    else: # sub button이 있는 경우
        try:
            # driver.find_element_by_xpath("//*[@id='content']/div/ul/li["+str(mainct_num)+"]/div[2]/div/ul/li/ul/li/span/span/a[3]")
            driver.find_element_by_css_selector("#content > div > ul > li.minutes_open > div.open_wrap02 > div > ul > li > ul > li > span > span > a:nth-child(3)")
            time.sleep(0.25)

            return 3 # sub button 하나 + 항목 하나
        except NoSuchElementException:
            try:
                driver.find_element_by_css_selector("#content > div > ul > li.minutes_open > div.open_wrap02 > div > ul > li > ul > li:nth-child(1) > span > span > a:nth-child(3)")
                return 4 # sub button 하나 + 항목 여러개
            except NoSuchElementException:
                try:
                    driver.find_element_by_css_selector("#content > div > ul > li.minutes_open > div.open_wrap02 > div > ul > li:nth-child(1) > ul > li > span > span > a:nth-child(3)")
                    return 5 # sub button 여러개 + 항목 하나
                except NoSuchElementException:
                    try:
                        driver.find_element_by_css_selector("#content > div > ul > li.minutes_open > div.open_wrap02 > div > ul > li:nth-child(1) > ul > li:nth-child(1) > span > span > a:nth-child(3)")
                        return 6 # sub button 여러개 + 항목 여러개
                    except NoSuchElementException:
                        return False


def urlinfo_cont(driver, flag, mainct_num, subct_num, content_num, daeList, daeClassList, sub_title):
    try:
        if flag==1:
            main_elem=driver.find_element_by_xpath("//*[@id='content']/div/ul/li["+str(mainct_num)+"]/div[2]/div/ul/li["+str(content_num)+"]/span/span/a[3]")
            elem=main_elem.get_attribute("onclick")
            text_elem=driver.find_element_by_xpath("//*[@id='content']/div/ul/li["+str(mainct_num)+"]/div[2]/div/ul/li["+str(content_num)+"]/span/a")
            # print(elem)
        else:
            main_elem=driver.find_element_by_xpath("//*[@id='content']/div/ul/li["+str(mainct_num)+"]/div[2]/div/ul/li["+str(subct_num)+"]/ul/li["+str(content_num)+"]/span/span/a[3]")
            elem=main_elem.get_attribute("onclick")
            text_elem=driver.find_element_by_xpath("//*[@id='content']/div/ul/li["+str(mainct_num)+"]/div[2]/div/ul/li["+str(subct_num)+"]/ul/li["+str(content_num)+"]/span/a[1]")
            # print(elem)

        if elem is None:
            # print("text not exist")
            pass
        else:
            elem=elem.split("'")
            if len(elem[3])<2:
                elem[3]="0"+elem[3]
            if len(elem[5])<3:
                while len(elem[5])<3:
                    elem[5]="0"+elem[5]
            if len(elem[7])<2:
                elem[7]="0"+elem[7]
            
            year=(text_elem.text.split('(')[1]).split("년")[0]
            month=(text_elem.text.split("년")[1]).split("월")[0]
            day=(text_elem.text.split("월")[1]).split("일")[0]
            text_title=year+month+day
            
            lock.acquire()

            global url_info
            global urlinfo_index
            url_info["mc"].append(elem[1])
            url_info["ct1"].append(elem[3])
            url_info["ct2"].append(elem[5])
            url_info["ct3"].append(elem[7])

            index=urlinfo_index

            # global 확인
            # print("mc : "+str(len(url_info["mc"]))+" "+url_info["mc"][urlinfo_index])
            # print("ct1 : "+str(len(url_info["ct1"]))+" "+url_info["ct1"][urlinfo_index])
            # print("ct2 : "+str(len(url_info["ct2"]))+" "+url_info["ct2"][urlinfo_index])
            # print("ct3 : "+str(len(url_info["ct3"]))+" "+url_info["ct3"][urlinfo_index])
            urlinfo_index=urlinfo_index+1

            lock.release()

            thread_down=DownText(index, daeList, daeClassList, sub_title, text_title)
            thread_down.setDaemon(True)
            thread_down.start()
            thread_down.join()
            
        return True       
    except NoSuchElementException:
        return False

def move_subcontent(driver, mainct_num, subct_num, daeList, daeClassList, sub_title):
    content_num=1

    try:
        # main_elem=driver.find_element_by_xpath("//*[@id='content']/div/ul/li["+str(mainct_num)+"]/div[2]/div/ul/li["+str(subct_num)+"]/a")
        main_elem=driver.find_element_by_css_selector("#content > div > ul > li:nth-child("+str(mainct_num)+") > div.open_wrap02 > div > ul > li:nth-child("+str(subct_num)+") > a")
        time.sleep(0.25)
        main_elem.click()
        time.sleep(0.25)
        
        ctonly_flag=check_ctonly(driver, mainct_num, subct_num, 1)

        while urlinfo_cont(driver, ctonly_flag, mainct_num, subct_num, content_num, daeList, daeClassList, sub_title):
            content_num+=1
        
        time.sleep(0.25)
        main_elem.click()
        time.sleep(0.25)
        return True
    except NoSuchElementException:
        return False

def move_content(driver, mainct_num, content_num, daeList, daeClassList):
    subcontent_num=1
    subcontent_flag=False
    
    try:
        # main_elem=driver.find_element_by_xpath("//*[@id='content']/div/ul/li["+str(content_num)+"]/div/a")
        main_elem=driver.find_element_by_css_selector("#content > div > ul > li:nth-child("+str(content_num)+") > div > a")
        time.sleep(0.25)
        sub_title=main_elem.text
        main_elem.click()
        time.sleep(0.25)

        while move_subcontent(driver, content_num, subcontent_num, daeList, daeClassList, sub_title):
            subcontent_flag=True
            subcontent_num+=1
        
        if not subcontent_flag:
            ctonly_flag=check_ctonly(driver, content_num, 0, 0)
            content_num2=1
            while urlinfo_cont(driver, ctonly_flag, content_num, 0, content_num2, daeList, daeClassList, None):
                content_num2+=1
        
        time.sleep(0.25)
        main_elem.click()
        time.sleep(0.25)
        return True
    except NoSuchElementException:
        return False

def move_commMenu(driver, _type, main_num, num, daeList, daeClassList):
    content_num=1
    
    try:
        # main_elem=driver.find_element_by_xpath("//*[@id='daeClassList']/ul/li["+str(main_num)+"]/a")
        main_elem=driver.find_element_by_css_selector("#daeClassList > ul > li.tabover.ranksta > a")
        time.sleep(0.25)
        main_elem.click()
        time.sleep(0.25)
        # elem=driver.find_element_by_xpath("//*[@id='"+_type+"']/li["+str(num)+"]/a")
        elem=driver.find_element_by_css_selector("#"+_type+" > li:nth-child("+str(num)+") > a")
        daeClassList=daeClassList+"-"+driver.find_element_by_css_selector("#"+_type+" > li:nth-child("+str(num)+") > a").text
        time.sleep(0.25)
        elem.click()
        time.sleep(0.25)
        
        while move_content(driver, main_num, content_num, daeList, daeClassList):
            content_num+=1
        
        return True
    except NoSuchElementException or ElementNotInteractableException:
        # main_elem.click()
        # time.sleep(0.25)
        # return False
        try:
            if num==1:
                elem=driver.find_element_by_css_selector("#"+_type+" > li > a")
                daeClassList=daeClassList+"-"+driver.find_element_by_css_selector("#"+_type+" > li > a").text
                time.sleep(0.25)
                elem.click()
                time.sleep(0.25)

                while move_content(driver, main_num, content_num, daeList, daeClassList):
                    content_num+=1
            else:
                main_elem.click()
                time.sleep(0.25)
            
            return False
        except NoSuchElementException or ElementNotInteractableException:
            main_elem.click()
            time.sleep(0.25)
            return False

def move_daeClassList(driver, num, page_flag, daeList):
    flag=False
    sub_flag=False
    sub_num=1
    content_num=1
    
    try:
        # elem = driver.find_element_by_xpath("//*[@id='daeClassList']/ul/li["+str(num)+"]/a")
        if num==1:
            elem = driver.find_element_by_css_selector("#daeClassList > ul > li.tabover > a")
            daeClassList=elem.text
        else:
            elem = driver.find_element_by_css_selector("#daeClassList > ul > li:nth-child("+str(num)+") > a")
            daeClassList=elem.text
            time.sleep(0.25)
            elem.click()
            time.sleep(0.25)

        if daeClassList=="소위원회" or daeClassList=="공청회" or daeClassList=="청문회" or daeClassList=="국정조사":
            return False
        flag=True

        if check_confirmCommMenu(driver, page_flag):
            sub_flag=True
            _type="ulConfirmCommMenu"
        # elif check_subCommMenu(driver, page_flag):
        #     sub_flag=True
        #     _type="ul_realrank_area"
        elif check_publicCommMenu(driver, page_flag):
            sub_flag=True
            _type="ulPublicCommMenu"
        elif check_hearingCommMenu(driver, page_flag):
            sub_flag=True
            _type="ulHearingCommMenu"
            
        
        if sub_flag:
            while move_commMenu(driver, _type, num, sub_num, daeList, daeClassList):
                sub_num=sub_num+1
        else:
            while move_content(driver, num, content_num, daeList, daeClassList):
                content_num+=1
                
        
        return flag
    except NoSuchElementException:
        if flag:
            return True
        else:
            return False

def move_daeList(driver, num):
    daeClassList_num=1
    if num>=7:
        page_flag=True
    else:
        page_flag=False
    
    try:
        # elem = driver.find_element_by_xpath("//*[@id='daeList']/li["+str(num)+"]/a")
        if num<=2:
            elem = driver.find_element_by_css_selector("#daeList > li.highlighting > a")
            daeList=elem.text.split('(')[0]
            time.sleep(0.25)
            elem.click()
            time.sleep(0.25)
        else:
            elem = driver.find_element_by_css_selector("#daeList > li:nth-child("+str(num)+") > a")
            daeList=elem.text.split('(')[0]
            time.sleep(0.25)
            elem.click()
            time.sleep(0.25)
            
        while move_daeClassList(driver, daeClassList_num, page_flag, daeList):
            daeClassList_num+=1

        # elem = driver.find_element_by_xpath("//*[@id='daeClassList']/ul/li[1]/a")
        elem = driver.find_element_by_css_selector("#daeClassList > ul > li:nth-child(1) > a")
        time.sleep(0.25)
        elem.click()
        time.sleep(0.25)
        
        return True
    except NoSuchElementException:
        print("finish")
        return False

class Multi(threading.Thread):
    def __init__(self, start_page):
        threading.Thread.__init__(self)
        self.start_page=start_page

    def stop(self):
        self._Thread__stop()

    def run(self):
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument('--headless')
        firefox_options.add_argument('--no-sandbox')
        firefox_options.add_argument('--disable-dev-shm-usage')
        firefox_profile=webdriver.FirefoxProfile()
        firefox_profile.set_preference("browser.cache.disk.enable", False)
        firefox_profile.set_preference("browser.cache.memory.enable", False)
        firefox_profile.set_preference("browser.cache.offline.enable", False)
        firefox_profile.set_preference("network.http.use-cache", False)

        driver = webdriver.Firefox(options=firefox_options, firefox_profile=firefox_profile, executable_path="./geckodriver")
        driver.get("http://likms.assembly.go.kr/record/mhs-40-010.do")
        
        daeList_num=self.start_page

        flag=False
        
        while move_daeList(driver, daeList_num):
            if daeList_num==2:
                daeList_num=1
            if daeList_num==4 and not flag:
                flag=True
                daeList_num=2
            daeList_num=daeList_num+2

        time.sleep(3)
        driver.quit()

class DownText(threading.Thread):
    def __init__(self, index, daeList, daeClassList, sub_title, title):
        threading.Thread.__init__(self)
        self.index=index
        self.daeList=daeList
        self.daeClassList=daeClassList
        self.sub_title=sub_title
        self.title=title

    def run(self):
        ui_index=self.index
        # path = url_info["mc"][ui_index]+"."+url_info["ct1"][ui_index]+"."+url_info["ct2"][ui_index]+"."+url_info["ct3"][ui_index]+"."
        if not os.path.isdir("./data/national_assembly/"+self.daeList+"/"):
            os.mkdir("./data/national_assembly/"+self.daeList+"/")
        if not os.path.isdir("./data/national_assembly/"+self.daeList+"/"+self.daeClassList+"/"):
            os.mkdir("./data/national_assembly/"+self.daeList+"/"+self.daeClassList+"/")
        if self.sub_title is not None and not os.path.isdir("./data/national_assembly/"+self.daeList+"/"+self.daeClassList+"/"+self.sub_title+"/"):
            os.mkdir("./data/national_assembly/"+self.daeList+"/"+self.daeClassList+"/"+self.sub_title+"/")
        
        flag=False
        pathFlag=False

        if self.sub_title is not None and os.path.isdir("./data/national_assembly/"+self.daeList+"/"+self.daeClassList+"/"+self.sub_title+"/"+self.title+"/"):
            # print("pass ===> ./data/national_assembly/"+self.daeList+"/"+self.daeClassList+"/"+self.sub_title+"/"+self.title+"/")
            pathFlag=True
            if os.path.isfile("./data/national_assembly/"+self.daeList+"/"+self.daeClassList+"/"+self.sub_title+"/"+self.title+"/"+self.title+".txt"):
                if os.path.getsize("./data/national_assembly/"+self.daeList+"/"+self.daeClassList+"/"+self.sub_title+"/"+self.title+"/"+self.title+".txt")==0:
                    # flag=True
                    pass
                else:
                    flag=True
                    print("pass ===> ./data/national_assembly/"+self.daeList+"/"+self.daeClassList+"/"+self.sub_title+"/"+self.title+"/")
        elif self.sub_title is None and os.path.isdir("./data/national_assembly/"+self.daeList+"/"+self.daeClassList+"/"+self.title+"/"):
            # print("pass ===> ./data/national_assembly/"+self.daeList+"/"+self.daeClassList+"/"+self.title+"/")
            pathFlag=True
            if os.path.isfile("./data/national_assembly/"+self.daeList+"/"+self.daeClassList+"/"+self.title+"/"+self.title+".txt"):
                if os.path.getsize("./data/national_assembly/"+self.daeList+"/"+self.daeClassList+"/"+self.title+"/"+self.title+".txt")==0:
                    # flag=True
                    pass
                else:
                    flag=True
                    print("pass ===> ./data/national_assembly/"+self.daeList+"/"+self.daeClassList+"/"+self.title+"/")

        if pathFlag==False and self.sub_title is None:
            os.mkdir("./data/national_assembly/"+self.daeList+"/"+self.daeClassList+"/"+self.title+"/")
            print("create ===> "+self.daeList+"/"+self.daeClassList+"/"+self.title+"/")
        elif pathFlag==False and self.sub_title is not None:
            os.mkdir("./data/national_assembly/"+self.daeList+"/"+self.daeClassList+"/"+self.sub_title+"/"+self.title+"/")
            print("create ===> "+self.daeList+"/"+self.daeClassList+"/"+self.sub_title+"/"+self.title+"/")
            
        # if self.sub_title is None:
        #     os.mkdir("./data/national_assembly/"+self.daeList+"/"+self.daeClassList+"/"+self.title+"/")
        #     print("create ===> "+self.daeList+"/"+self.daeClassList+"/"+self.title+"/")
        #     path="./data/national_assembly/"+self.daeList+"/"+self.daeClassList+"/"+self.title+"/"
        # else:
        #     os.mkdir("./data/national_assembly/"+self.daeList+"/"+self.daeClassList+"/"+self.sub_title+"/"+self.title+"/")
        #     print("create ===> "+self.daeList+"/"+self.daeClassList+"/"+self.sub_title+"/"+self.title+"/")
        #     path="./data/national_assembly/"+self.daeList+"/"+self.daeClassList+"/"+self.sub_title+"/"+self.title+"/"

        if flag==False:
            lock.acquire()
            global testCheck
            testCheck+=1
            lock.release()

            if self.sub_title is None:
                path="./data/national_assembly/"+self.daeList+"/"+self.daeClassList+"/"+self.title+"/"
            else:
                path="./data/national_assembly/"+self.daeList+"/"+self.daeClassList+"/"+self.sub_title+"/"+self.title+"/"
            firefox_options = webdriver.FirefoxOptions()
            firefox_options.add_argument('--headless')
            firefox_options.add_argument('--no-sandbox')
            firefox_options.add_argument('--disable-dev-shm-usage')
            firefox_profile=webdriver.FirefoxProfile()
            firefox_profile.set_preference("browser.cache.disk.enable", False)
            firefox_profile.set_preference("browser.cache.memory.enable", False)
            firefox_profile.set_preference("browser.cache.offline.enable", False)
            firefox_profile.set_preference("network.http.use-cache", False)

            url='https://w3.assembly.go.kr/jsp/vod/vod.do?cmd=vod&mc='+url_info["mc"][ui_index]+'&ct1='+url_info["ct1"][ui_index]+'&ct2='+url_info["ct2"][ui_index]+'&ct3='+url_info["ct3"][ui_index]

            driver = webdriver.Firefox(options=firefox_options, firefox_profile=firefox_profile, executable_path="./geckodriver")
            driver.get(url)

            text_index=1
            text=""
            try:
                while True:
                    textSub=""
                    textSub=textSub+driver.find_element_by_css_selector("#sm"+str(text_index)).text

                    puri=purifyText(textSub)
                    if puri is not None:
                        text=text+puri

                    text_index+=1
            except NoSuchElementException:
                file_path=path+self.title+".txt"
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

    thread_1=Multi(2)
    thread_2=Multi(4)

    thread_1.setDaemon(True)
    thread_2.setDaemon(True)

    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()

    # global url_info
    # print("total text : "+str(len(url_info["mc"])))
    global testCheck
    print("check : "+testCheck)

# if __name__ == '__main__':
#     main()