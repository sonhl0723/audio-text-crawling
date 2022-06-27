from assembly.conf import *
from assembly.utils import prep_text

url_info = {"mc":[], "ct1":[], "ct2":[], "ct3":[]}
urlinfo_index=0
test_check=0

lock=threading.Lock()

def check_confirmCommMenu(driver, page_flag):
    if page_flag:
        try:
            elem=driver.find_element_by_css_selector("#confirmCommMenu")
            time.sleep(0.25)
            elem.click()
            time.sleep(0.25)
            return True
        except NoSuchElementException: return False
    else:
        try:
            elem=driver.find_element_by_css_selector("#confirmCommMenu")
            time.sleep(0.25)
            elem.click()
            time.sleep(0.25)
            return True
        except ElementNotInteractableException or NoSuchElementException: return False

def check_publicCommMenu(driver, page_flag):
    try:
        elem=driver.find_element_by_css_selector("#publicCommMenu")
        time.sleep(0.25)
        elem.click()
        time.sleep(0.25)
        return True
    except ElementNotInteractableException or NoSuchElementException: return False

def check_hearingCommMenu(driver, page_flag):
    if page_flag:
        try:
            elem=driver.find_element_by_css_selector("#hearingCommMenu")
            time.sleep(0.25)
            elem.click()
            time.sleep(0.25)
            return True
        except ElementNotInteractableException or NoSuchElementException: return False
    else:
        try:
            elem=driver.find_element_by_css_selector("#hearingCommMenu")
            time.sleep(0.25)
            elem.click()
            time.sleep(0.25)
            return True
        except ElementNotInteractableException or NoSuchElementException: return False

def check_ctonly(driver, mainct_num, subct_num, sub_flag):
    if sub_flag==0: # sub button이 없는 경우
        try:
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


def urlinfo_cont(driver, flag, mainct_num, subct_num, content_num, dae_list, dae_class_list, sub_title):
    try:
        if flag==1:
            main_elem=driver.find_element_by_xpath("//*[@id='content']/div/ul/li["+str(mainct_num)+"]/div[2]/div/ul/li["+str(content_num)+"]/span/span/a[3]")
            elem=main_elem.get_attribute("onclick")
            text_elem=driver.find_element_by_xpath("//*[@id='content']/div/ul/li["+str(mainct_num)+"]/div[2]/div/ul/li["+str(content_num)+"]/span/a")
        else:
            main_elem=driver.find_element_by_xpath("//*[@id='content']/div/ul/li["+str(mainct_num)+"]/div[2]/div/ul/li["+str(subct_num)+"]/ul/li["+str(content_num)+"]/span/span/a[3]")
            elem=main_elem.get_attribute("onclick")
            text_elem=driver.find_element_by_xpath("//*[@id='content']/div/ul/li["+str(mainct_num)+"]/div[2]/div/ul/li["+str(subct_num)+"]/ul/li["+str(content_num)+"]/span/a[1]")

        if elem is None: pass
        else:
            elem=elem.split("'")
            if len(elem[3])<2: elem[3]="0"+elem[3]
            if len(elem[5])<3:
                while len(elem[5])<3: elem[5]="0"+elem[5]
            if len(elem[7])<2: elem[7]="0"+elem[7]
            
            year=(text_elem.text.split('(')[1]).split("년")[0]
            month=(text_elem.text.split("년")[1]).split("월")[0]
            day=(text_elem.text.split("월")[1]).split("일")[0]
            text_title=year+month+day
            
            lock.acquire()

            global url_info, urlinfo_index
            url_info["mc"].append(elem[1])
            url_info["ct1"].append(elem[3])
            url_info["ct2"].append(elem[5])
            url_info["ct3"].append(elem[7])

            index=urlinfo_index

            urlinfo_index=urlinfo_index+1

            lock.release()

            thread_down=DownText(index, dae_list, dae_class_list, sub_title, text_title)
            thread_down.setDaemon(True)
            thread_down.start()
            thread_down.join()
            
        return True       
    except NoSuchElementException: return False

def move_subcontent(driver, mainct_num, subct_num, dae_list, dae_class_list, sub_title):
    content_num=1

    try:
        main_elem=driver.find_element_by_css_selector("#content > div > ul > li:nth-child("+str(mainct_num)+") > div.open_wrap02 > div > ul > li:nth-child("+str(subct_num)+") > a")
        time.sleep(0.25)
        main_elem.click()
        time.sleep(0.25)
        
        ctonly_flag=check_ctonly(driver, mainct_num, subct_num, 1)

        while urlinfo_cont(driver, ctonly_flag, mainct_num, subct_num, content_num, dae_list, dae_class_list, sub_title): content_num+=1
        
        time.sleep(0.25)
        main_elem.click()
        time.sleep(0.25)
        return True
    except NoSuchElementException: return False

def move_content(driver, mainct_num, content_num, dae_list, dae_class_list):
    subcontent_num=1
    subcontent_flag=False
    
    try:
        main_elem=driver.find_element_by_css_selector("#content > div > ul > li:nth-child("+str(content_num)+") > div > a")
        time.sleep(0.25)
        sub_title=main_elem.text
        main_elem.click()
        time.sleep(0.25)

        while move_subcontent(driver, content_num, subcontent_num, dae_list, dae_class_list, sub_title):
            subcontent_flag=True
            subcontent_num+=1
        
        if not subcontent_flag:
            ctonly_flag=check_ctonly(driver, content_num, 0, 0)
            content_num2=1
            while urlinfo_cont(driver, ctonly_flag, content_num, 0, content_num2, dae_list, dae_class_list, None): content_num2+=1
        
        time.sleep(0.25)
        main_elem.click()
        time.sleep(0.25)
        return True
    except NoSuchElementException: return False

def move_commMenu(driver, _type, main_num, num, dae_list, dae_class_list):
    content_num=1
    
    try:
        main_elem=driver.find_element_by_css_selector("#daeClassList > ul > li.tabover.ranksta > a")
        time.sleep(0.25)
        main_elem.click()
        time.sleep(0.25)

        elem=driver.find_element_by_css_selector("#"+_type+" > li:nth-child("+str(num)+") > a")
        dae_class_list=dae_class_list+"-"+driver.find_element_by_css_selector("#"+_type+" > li:nth-child("+str(num)+") > a").text
        time.sleep(0.25)
        elem.click()
        time.sleep(0.25)
        
        while move_content(driver, main_num, content_num, dae_list, dae_class_list): content_num+=1
        
        return True
    except NoSuchElementException or ElementNotInteractableException:
        try:
            if num==1:
                elem=driver.find_element_by_css_selector("#"+_type+" > li > a")
                dae_class_list=dae_class_list+"-"+driver.find_element_by_css_selector("#"+_type+" > li > a").text
                time.sleep(0.25)
                elem.click()
                time.sleep(0.25)

                while move_content(driver, main_num, content_num, dae_list, dae_class_list): content_num+=1
            else:
                main_elem.click()
                time.sleep(0.25)
            
            return False
        except NoSuchElementException or ElementNotInteractableException:
            main_elem.click()
            time.sleep(0.25)
            return False

def move_daeClassList(driver, num, page_flag, dae_list):
    flag=False
    sub_flag=False
    sub_num=1
    content_num=1
    
    try:
        if num==1:
            elem = driver.find_element_by_css_selector("#daeClassList > ul > li.tabover > a")
            dae_class_list=elem.text
        else:
            elem = driver.find_element_by_css_selector("#daeClassList > ul > li:nth-child("+str(num)+") > a")
            dae_class_list=elem.text
            time.sleep(0.25)
            elem.click()
            time.sleep(0.25)

        if dae_class_list=="소위원회" or dae_class_list=="공청회" or dae_class_list=="청문회" or dae_class_list=="국정조사": return False

        flag=True

        if check_confirmCommMenu(driver, page_flag):
            sub_flag=True
            _type="ulConfirmCommMenu"
        elif check_publicCommMenu(driver, page_flag):
            sub_flag=True
            _type="ulPublicCommMenu"
        elif check_hearingCommMenu(driver, page_flag):
            sub_flag=True
            _type="ulHearingCommMenu"
            
        
        if sub_flag:
            while move_commMenu(driver, _type, num, sub_num, dae_list, dae_class_list): sub_num=sub_num+1
        else:
            while move_content(driver, num, content_num, dae_list, dae_class_list): content_num+=1
                
        
        return flag
    except NoSuchElementException:
        if flag: return True
        else: return False

def move_daeList(driver, num):
    daeClassList_num=1
    if num>=7: page_flag=True
    else: page_flag=False
    
    try:
        if num<=2:
            elem = driver.find_element_by_css_selector("#daeList > li.highlighting > a")
            dae_list=elem.text.split('(')[0]
            time.sleep(0.25)
            elem.click()
            time.sleep(0.25)
        else:
            elem = driver.find_element_by_css_selector("#daeList > li:nth-child("+str(num)+") > a")
            dae_list=elem.text.split('(')[0]
            time.sleep(0.25)
            elem.click()
            time.sleep(0.25)
            
        while move_daeClassList(driver, daeClassList_num, page_flag, dae_list): daeClassList_num+=1

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

    def stop(self): self._Thread__stop()

    def run(self):
        # --------------------------------------------------firefox
        firefox_options = webdriver.FirefoxOptions()
        for option in webdriver_option: firefox_options.add_argument(option)
        firefox_profile=webdriver.FirefoxProfile()
        for prof in webdriver_profile: firefox_profile.set_preference(prof, False)
        driver = webdriver.Firefox(options=firefox_options, firefox_profile=firefox_profile, executable_path="./geckodriver")
        # --------------------------------------------------firefox

        driver.get(conf_data["MAIN_COUNCIL_URL"])
        
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
    def __init__(self, index, dae_list, dae_class_list, sub_title, title):
        threading.Thread.__init__(self)
        self.index=index
        self.dae_list=dae_list
        self.dae_class_list=dae_class_list
        self.sub_title=sub_title
        self.title=title

    def run(self):
        ui_index=self.index
        if not os.path.isdir(base_path+self.dae_list+"/"): os.mkdir(base_path+self.dae_list+"/")
        if not os.path.isdir(base_path+self.daeList+"/"+self.dae_class_list+"/"): os.mkdir(base_path+self.dae_list+"/"+self.dae_class_list+"/")
        if self.sub_title is not None and not os.path.isdir(base_path+self.dae_list+"/"+self.dae_class_list+"/"+self.sub_title+"/"):
            os.mkdir(base_path+self.dae_list+"/"+self.dae_class_list+"/"+self.sub_title+"/")
        
        flag=False
        path_flag=False

        if self.sub_title is not None and os.path.isdir(base_path+self.dae_list+"/"+self.dae_class_list+"/"+self.sub_title+"/"+self.title+"/"):
            path_flag=True
            if os.path.isfile(base_path+self.dae_list+"/"+self.dae_class_list+"/"+self.sub_title+"/"+self.title+"/"+self.title+".txt"):
                if os.path.getsize(base_path+self.dae_list+"/"+self.dae_class_list+"/"+self.sub_title+"/"+self.title+"/"+self.title+".txt")==0: pass
                else:
                    flag=True
                    print("pass ===> "+base_path+self.dae_list+"/"+self.dae_class_list+"/"+self.sub_title+"/"+self.title+"/")
        elif self.sub_title is None and os.path.isdir(base_path+self.dae_list+"/"+self.dae_class_list+"/"+self.title+"/"):
            path_flag=True
            if os.path.isfile(base_path+self.dae_list+"/"+self.dae_class_list+"/"+self.title+"/"+self.title+".txt"):
                if os.path.getsize(base_path+self.dae_list+"/"+self.dae_class_list+"/"+self.title+"/"+self.title+".txt")==0: pass
                else:
                    flag=True
                    print("pass ===> "+base_path+self.dae_list+"/"+self.dae_class_list+"/"+self.title+"/")

        if path_flag==False and self.sub_title is None:
            os.mkdir(base_path+self.dae_list+"/"+self.dae_class_list+"/"+self.title+"/")
            print("create ===> "+self.dae_list+"/"+self.dae_class_list+"/"+self.title+"/")
        elif path_flag==False and self.sub_title is not None:
            os.mkdir(base_path+self.dae_list+"/"+self.dae_class_list+"/"+self.sub_title+"/"+self.title+"/")
            print("create ===> "+self.dae_list+"/"+self.dae_class_list+"/"+self.sub_title+"/"+self.title+"/")

        if flag==False:
            lock.acquire()
            global test_check
            test_check+=1
            lock.release()

            if self.sub_title is None: path=base_path+self.dae_list+"/"+self.dae_class_list+"/"+self.title+"/"
            else: path=base_path+self.dae_list+"/"+self.dae_class_list+"/"+self.sub_title+"/"+self.title+"/"

            # --------------------------------------------------firefox
            firefox_options = webdriver.FirefoxOptions()
            for option in webdriver_option: firefox_options.add_argument(option)
            firefox_profile=webdriver.FirefoxProfile()
            for prof in webdriver_profile: firefox_profile.set_preference(prof, False)
            driver = webdriver.Firefox(options=firefox_options, firefox_profile=firefox_profile, executable_path="./geckodriver")
            # --------------------------------------------------firefox

            url=conf_data["TEXT_BASE_URL"]+url_info["mc"][ui_index]+'&ct1='+url_info["ct1"][ui_index]+'&ct2='+url_info["ct2"][ui_index]+'&ct3='+url_info["ct3"][ui_index]

            driver.get(url)

            text_index=1
            text=""
            try:
                while True:
                    text_sub=""
                    text_sub=textSub+driver.find_element_by_css_selector("#sm"+str(text_index)).text

                    puri=prep_text(text_sub)
                    if puri is not None: text=text+puri

                    text_index+=1
            except NoSuchElementException:
                file_path=path+self.title+".txt"
                Path(file_path).touch()
                text_file = open(file_path, "a")
                text_file.write(text)
                text_file.close()
                driver.quit()

def main():
    if not os.path.isdir('../data/'): os.mkdir('../data/')
    if not os.path.isdir(base_path): os.mkdir(base_path)

    thread_1=Multi(2)
    thread_2=Multi(4)

    thread_1.setDaemon(True)
    thread_2.setDaemon(True)

    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()

    global test_check
    print("check : "+str(test_check))