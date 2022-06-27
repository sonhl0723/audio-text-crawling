from tvchosun.conf import *
from tvchosun.download_main import download_audio, download_text
from tvchosun.utils import wrong_date_check
import tvchosun.tvcs_9_remain

def collect_text_url(url):
    page_num=1
    text_url=[]

    while True:
        detailed_url=url+"&pn="+str(page_num)
        s=requests.session()
        s.keep_alive=False
        response=s.get(detailed_url)
        html=response.text
        soup=BeautifulSoup(html, 'html.parser')

        for i in soup.select('#iframe > div.bbs_zine.top_line > ul > li > div.detail > p.article_tit > a'):
            elem=i.get("onclick").split("'")[1].split("'")[0]
            if not elem.find("vir")!=-1: text_url.append(elem)

        page_num+=1
        detailed_url=url+"&pn="+str(page_num)
        if wrong_date_check(detailed_url): break

    return text_url

def current_date_check(url):
    s=requests.session()
    s.keep_alive=False
    response=s.get(url)

    if response.status_code == 200:
        html=response.text
        soup=BeautifulSoup(html, 'html.parser')
        iframe_src=soup.select_one("#favnews_frame").attrs["src"]

        response_iframe=requests.get("http:"+iframe_src)
        htmlIframe=response_iframe.text
        soupIframe=BeautifulSoup(htmlIframe, 'html.parser')
        currentDate=soupIframe.select_one("#iframe > div.newstop_area > p").get_text().split("(")[0].split(".")
        
        return current_date
    else: print(response.status_code)

def main():
    if not os.path.isdir('../data/'): os.mkdir('../data/')
    if not os.path.isdir(base_path): os.mkdir(base_path)

    news9={"current_date":[], "date_list":[]}
    news7={"current_date":[], "dtae_list":[]}
    last_date=conf_data['LAST_DATE']
    
    news9["current_date"]=current_date_check(news9["url"])
    news7["current_date"]=current_date_check(news7["url"])

    for i in last_date:
        if not os.path.isdir(base_path+str(i)+"/"): os.mkdir(base_path+str(i)+"/")
        last_year=last_date[i][0]
        last_month=last_date[i][1]
        last_day=last_date[i][2]

        if i=="news9":
            year=news9["current_date"][0]
            month=news9["current_date"][1]
            day=news9["current_date"][2]
        else:
            year=news7["current_date"][0]
            month=news7["current_date"][1]
            day=news7["current_date"][2]

        if i=="news9":
            base_url=conf_data["NEWS9_URL"][0]
            audio_base_url=conf_data["NEWS9_URL"][1]
        else:
            base_url=conf_data["NEWS7_URL"][0]
            audio_base_url=conf_data["NEWS7_URL"][1]

        check_total=0
        check_wrong=0

        while True:
            url=base_url+year+month+day
            audio_down_flag=True

            if not wrong_date_check(url):
                text_url_list=collect_text_url(url)

                audio_down_flag=download_audio(audio_base_url, str(i), year+month+day)
                if audio_down_flag:
                    final_text=""
                    for text_url in text_url_list: download_text(text_url, str(i), year+month+day, final_text)

                    check_total+=1
                else: print("Already Downloaded")

            else: check_wrong+=1

            if day=="01":
                day="31"
                month=str(int(month)-1)

                if month=="0":
                    month="12"
                    year=str(int(year)-1)
                elif len(month)==1: month="0"+month
            else:
                day=str(int(day)-1)
                if len(day)==1: day="0"+day

            if int(year+month+day)<int(last_year+last_month+last_day):
                print(i+" checkTotal:"+str(check_total))
                break

    tvcs_9_remain.main()