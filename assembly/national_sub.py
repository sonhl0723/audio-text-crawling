from assembly.conf import *
from assembly.utils import prep_text, define_council

url_list = {"mc":[], "ct1":[], "ct2":[], "ct3":[], "dae_class_list":[], "sub_content":[], "title":[]}
url_list_index=0
real_title=""
inspect_flag=False

dae_list=""

def url_info(driver, content_index):
    global url_list, url_list_index, dae_list, real_title
    try:
        check=driver.find_element_by_css_selector("body > div.sectionBox2_03 > div > div.rightmenu > div.contenttext_box > div.doard > table > tbody > tr:nth-child("+str(content_index)+") > td.td_last > a > img")
        time.sleep(0.25)
        title=driver.find_element_by_css_selector("body > div.sectionBox2_03 > div > div.rightmenu > div.contenttext_box > div.doard > table > tbody > tr:nth-child("+str(content_index)+") > td:nth-child(1)").text.replace("-","")
        dae_class_list=driver.find_element_by_css_selector("body > div.sectionBox2_03 > div > div.rightmenu > div.contenttext_box > div.doard > table > tbody > tr:nth-child("+str(content_index)+") > td:nth-child(5)").text
        if len(dae_class_list)>3 and (dae_class_list[0:3]=="청문회" or dae_class_list[0:3]=="공청회"): dae_class_list=dae_class_list[0:3]
        sub_content=driver.find_element_by_css_selector("body > div.sectionBox2_03 > div > div.rightmenu > div.contenttext_box > div.doard > table > tbody > tr:nth-child("+str(content_index)+") > td:nth-child(3)").text
        sub_content=define_council(sub_content)

        if dae_class_list.find("국정")!=-1: real_title=driver.find_element_by_css_selector("body > div.sectionBox2_03 > div > div.rightmenu > div.contenttext_box > div.doard > table > tbody > tr:nth-child("+str(content_index)+") > td.td_last > a").text
  
        elem=driver.find_element_by_css_selector("body > div.sectionBox2_03 > div > div.rightmenu > div.contenttext_box > div.doard > table > tbody > tr:nth-child("+str(content_index)+") > td.td_last > a").get_attribute("href")
        elem=elem.split("'")
        if len(elem[3])<2: elem[3]="0"+elem[3]
        if len(elem[5])<3:
            while len(elem[5])<3: elem[5]="0"+elem[5]
        if len(elem[7])<2: elem[7]="0"+elem[7]

        url_list["mc"].append(elem[1])
        url_list["ct1"].append(elem[3])
        url_list["ct2"].append(elem[5])
        url_list["ct3"].append(elem[7])
        url_list["dae_class_list"].append(dae_class_list)
        url_list["sub_content"].append(sub_content)
        url_list["title"].append(title)

        thread_down=DownText(url_list_index, dae_list)
        thread_down.setDaemon(True)
        thread_down.start()
        thread_down.join()

        url_list_index=url_list_index+1
        
        return True
    except NoSuchElementException:
        if content_index<=10:
            print("영상이 존재하지 않음")
            return True
        else: return False

def move_number_next(driver, number_index):
    content_index=1
    try:
        if not content_index==1:
            numberElem=driver.find_element_by_css_selector("body > div.sectionBox2_03 > div > div.rightmenu > div.contenttext_box > div.divPaging > div > a:nth-child("+str(content_index+2)+")")
            time.sleep(0.25)
            numberElem.click()
            time.sleep(0.25)

        while url_info(driver, content_index): content_index+=1

        if content_index%10==0:
            numberElem=driver.find_element_by_css_selector("body > div.sectionBox2_03 > div > div.rightmenu > div.contenttext_box > div.divPaging > div > a:nth-child("+str(content_index+3)+")")
            time.sleep(0.25)
            numberElem.click()
            time.sleep(0.25)

        return content_index
    except NoSuchElementException: return False

    

def move_sheight(driver, sheight_index):
    number_index=1
    content_index=1
    global dae_list

    try:
        if not sheight_index==1:
            sheight_elem=driver.find_element_by_css_selector("#sheight > dl > dt:nth-child("+str(sheight_index)+")")
            time.sleep(0.25)
            dae_list="제"+sheight_elem.text.split(" ")[0]
            sheight_elem.click()
            time.sleep(0.25)
        else:
            dae_list="제"+driver.find_element_by_css_selector("#sheight > dl > dt:nth-child(1) > a").text.split(" ")[0]

        last_page=int(driver.find_element_by_xpath("//*[@title='마지막 페이지']").get_attribute("href").split("'")[1].split("'")[0])
        time.sleep(0.25)

        while url_info(driver, content_index): content_index+=1
        
        while last_page>0:
            number_index=move_number_next(driver, number_index)

            if number_index%10==0: number_index=1
            else: number_index+=1

            last_page-=1

        return True
    except NoSuchElementException:
        return False

def move_menu_copy():
    global inspect_flag

    # --------------------------------------------------firefox
    firefox_options = webdriver.FirefoxOptions()
    for option in webdriver_option: firefox_options.add_argument(option)
    firefox_profile=webdriver.FirefoxProfile()
    for prof in webdriver_profile: firefox_profile.set_preference(prof, False)
    driver = webdriver.Firefox(options=firefox_options, firefox_profile=firefox_profile, executable_path="./geckodriver")
    # --------------------------------------------------firefox

    driver.get(conf_data["MAIN_PAGE"])
    driver.switch_to.frame(driver.find_element_by_name("down"))

    hearing_elem=driver.find_element_by_css_selector("#hederBox_01 > div.h1box_02 > ul > li:nth-child(7)")

    sheight_index=1
    time.sleep(0.25)
    hearing_elem.click()
    time.sleep(0.25)

    while move_sheight(driver, sheight_index):
        sheight_index+=1
        if sheight_index==2: sheight_index=3
        
    inspect_elem=driver.find_element_by_css_selector("#hederBox_01 > div.h1box_02 > ul > li:nth-child(8)")
    inspect_flag=True
    time.sleep(0.25)
    sheight_index=6
    inspect_elem.click()
    time.sleep(0.25)

    while move_sheight(driver, sheight_index):
        sheight_index+=1
        if sheight_index==2: sheight_index=3
    
class DownText(threading.Thread):
    global url_list, real_title, inspect_flag

    def __init__(self, url_list_index, dae_list):
        threading.Thread.__init__(self)
        self.url_list_index=url_list_index
        self.dae_list=dae_list

    def run(self):
        dae_class_list=url_list["dae_class_list"][self.url_list_index]
        sub_content=url_list["sub_content"][self.url_list_index]
        title=url_list["title"][self.url_list_index]

        if not os.path.isdir(base_path+self.dae_list+"/"): os.mkdir(base_path+self.dae_list+"/")
        if not os.path.isdir(base_path+self.dae_list+"/"+dae_class_list+"/"): os.mkdir(base_path+self.dae_list+"/"+dae_class_list+"/")
        if not os.path.isdir(base_path+self.dae_list+"/"+dae_class_list+"/"+sub_content+"/"): os.mkdir(base_path+self.dae_list+"/"+dae_class_list+"/"+sub_content+"/")    
        if not os.path.isdir(base_path+self.dae_list+"/"+dae_class_list+"/"+sub_content+"/"+title+"/"): os.mkdir(base_path+self.dae_list+"/"+dae_class_list+"/"+sub_content+"/"+title+"/")

        flag=False
        if not inspect_flag and os.path.isfile(base_path+self.dae_list+"/"+dae_class_list+"/"+sub_content+"/"+title+"/"+title+".txt"):
            if os.path.getsize(base_path+self.dae_list+"/"+dae_class_list+"/"+sub_content+"/"+title+"/"+title+".txt")==0:
                os.remove(base_path+self.dae_list+"/"+dae_class_list+"/"+sub_content+"/"+title+"/"+title+".txt")
                flag=True
            else:
                print("pass ===> "+base_path+self.dae_list+"/"+dae_class_list+"/"+sub_content+"/"+title+"/")
                pass
        elif inspect_flag and os.path.isfile(base_path+self.dae_list+"/"+dae_class_list+"/"+sub_content+"/"+title+"/"+real_title+".txt"):
            if not os.path.getsize(base_path+self.dae_list+"/"+dae_class_list+"/"+sub_content+"/"+title+"/"+real_title+".txt")==0:
                os.remove(base_path+self.dae_list+"/"+dae_class_list+"/"+sub_content+"/"+title+"/"+real_title+".txt")
                flag=True
            else:
                print("pass ===> "+base_path+self.dae_list+"/"+dae_class_list+"/"+sub_content+"/"+title+"/"+real_title)
                pass
        if flag==True:
            path=base_path+self.dae_list+"/"+dae_class_list+"/"+sub_content+"/"+title+"/"

            # --------------------------------------------------firefox
            firefox_options = webdriver.FirefoxOptions()
            for option in webdriver_option: firefox_options.add_argument(option)
            firefox_profile=webdriver.FirefoxProfile()
            for prof in webdriver_profile: firefox_profile.set_preference(prof, False)
            driver = webdriver.Firefox(options=firefox_options, firefox_profile=firefox_profile, executable_path="./geckodriver")
            # --------------------------------------------------firefox

            url=conf_data["TEXT_BASE_URL"]+url_list["mc"][self.url_list_index]+'&ct1='+url_list["ct1"][self.url_list_index]+'&ct2='+url_list["ct2"][self.url_list_index]+'&ct3='+url_list["ct3"][self.url_list_index]

            driver.get(url)

            text_index=1
            text=""
            try:
                while True:
                    text_sub=""
                    text_sub=text_sub+driver.find_element_by_css_selector("#sm"+str(text_index)).text
                    time.sleep(0.25)

                    puri=prep_text(text_sub)
                    if puri is not None:
                        text=text+puri

                    text_index+=1
            except NoSuchElementException:
                if inspect_flag: file_path=path+real_title+".txt"
                else: file_path=path+title+".txt"

                Path(file_path).touch()
                print("create ===> "+file_path)
                text_file = open(file_path, "a")
                text_file.write(text)
                text_file.close()
                driver.quit()
            
def main():
    if not os.path.isdir('../data/'): os.mkdir('../data/')
    if not os.path.isdir(base_path): os.mkdir(base_path)

    move_menu_copy()

    print("total text : "+str(len(url_list["mc"])))