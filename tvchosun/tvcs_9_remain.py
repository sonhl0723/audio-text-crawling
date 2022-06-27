from tvchosun.conf import *
from tvchosun.download_remain import download_audio, download_text
from tvchosun.utils import wrong_date_check

def collect_text_url(url):
    page_num=1
    text_url=[]

    while True:
        detailedUrl=url+"&pn="+str(page_num)
        s=requests.session()
        s.keep_alive=False
        response=s.get(detailedUrl)
        # response=requests.get(detailedUrl)
        html=response.text
        soup=BeautifulSoup(html, 'html.parser')

        for i in soup.select('#iframe > div.bbs_zine.top_line > ul > li > div.detail > p.article_tit > a'):
            elem=i.get("onclick").split("'")[1].split("'")[0]
            if not elem.find("vir")!=-1:
                text_url.append(elem)

        page_num+=1
        detailed_url=url+"&pn="+str(page_num)
        if wrong_date_check(detailed_url): break

    return text_url

def main():
    last_date={"news9":["2013","03","04"]}

    for i in last_date:
        if not os.path.isdir(base_path+str(i)+"/"): os.mkdir(base_path+str(i)+"/")
        last_year=last_date[i][0]
        last_month=last_date[i][1]
        last_day=last_date[i][2]

        year="2016"
        month="05"
        day="24"

        base_url=conf_data["NEWS9_URL"][0]

        check_total=0
        check_wrong=0

        while True:
            url=base_url+year+month+day

            if not wrong_date_check(url):
                text_url_list=collect_text_url(url)
                text_url_list=text_url_list[1:]

                for text_url in text_url_list:
                    if download_audio(text_url, str(i), year+month+day):
                        download_text(text_url, str(i), year+month+day)

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