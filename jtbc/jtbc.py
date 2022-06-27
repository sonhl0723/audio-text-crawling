from jtbc.conf import *
from jtbc.utils import current_date_check
from jtbc.download import download_text

total_check = 0

def jtbc():
    global total_check
    if not os.path.isdir('../data/'): os.mkdir('../data/')
    if not os.path.isdir(base_path): os.mkdir(base_path)
    if not os.path.isdir(final_path): os.mkdir(final_path)

    date=current_date_check()
    year=date[0:4]
    month=date[4:6]
    day=date[6:]

    base_url = conf_data['CURRENT_URL'] + "&strSearchDate="
    title=[]
    last_year, last_month, last_day = last_date[0], last_date[1], last_date[2]

    while True:
        url=base_url+date

        if total_check%30==0: time.sleep(0.25)

        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        video_url=[]
        video = [i['href'] for i in soup.select('#form1 > div.news_main > div.review_list > div.bd > ul > li > div.lt > a')]
        if str(soup).find("1부")==-1:
            try:
                video_url.append(video[0])
            except IndexError:
                video_url.append(video[0])
        else:
            video_url=video[0:2]

        if len(video_url)>1:
            title.append(date+"_1")
            title.append(date+"_2")
            if not os.path.isdir(final_path+title[0]): os.mkdir(final_path+title[0])
            if not os.path.isdir(final_path+title[1]): os.mkdir(final_path+title[1])
        else:
            title.append(date)
            if not os.path.isdir(final_path+title[0]): os.mkdir(final_path+title[0])

        if download_text(video_url, title): total_check += 1

        video_url.clear()
        title.clear()

        if day=="01":
            month=str(int(month)-1)

            if month=="0":
                month="12"
                year=str(int(year)-1)
            elif len(month)==1: month="0"+month

            if month=="04" or month=="06" or month=="09" or month=="11": day="30"
            elif month=="02": day="28"
            else: day="31"

        else:
            day=str(int(day)-1)
            if len(day)==1: day="0"+day

        if int(year+month+day)<int(last_year+last_month+last_day):
            print("total: "+str(total_check))
            print("last_date: "+date)
            break

        date=year+month+day