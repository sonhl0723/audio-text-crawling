from ulsan.conf import *
from ulsan.download import plenary_download_audio_text

def plenary_meeting():

    only_num = re.compile('[^0-9]') # 날짜 전처리

    page_num = 1

    if os.path.isdir(base_path+"plenary meeting"):
        if os.path.isfile(base_path+"plenary meeting/20101112/ulsan_20101112.txt"):
            print("Download Completely => plenary meeting")
            return 0
    else: os.mkdir(base_path+"plenary meeting/")

    dir_path = base_path+"plenary meeting"

    total_video_href = []
    total_video_title = []
    total_mp3_path = []
    total_text_href = []
    total_text_title = []
    lost_something = ['20101112']

    while(1):
        url = 'http://www.council.ulsan.kr/cast/sub/general.do?pageIndex='+str(page_num)
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        page_link = [i.get("href") for i in soup.select('#divContents > div > section > div > div.general_left > div > ul > li > a')]
        for page in page_link:
            page_url = 'http://www.council.ulsan.kr'+page
            page_response = requests.get(page_url)
            page_html = page_response.text
            page_soup = BeautifulSoup(page_html, 'html.parser')
            in_link = [i.get("href") for i in page_soup.select('div.in ul.list_styleGeneral li.in a')]
            title = [i.get_text() for i in page_soup.select('#divContents > div > section > div > div.general_left > div > ul > li > a > span')]

            video_title_index = 0

            for link in in_link:
                link_url = 'http://www.council.ulsan.kr'+link
                link_response = requests.get(link_url)
                link_html = link_response.text
                link_soup = BeautifulSoup(link_html, 'html.parser')

                video_href = [i.get("href") for i in link_soup.select('div.in div.g_play a')]
                dir_name = only_num.sub('', title[video_title_index])
                video_title_index = video_title_index + 1
                if video_href[0] not in total_video_href:
                    total_video_href.append(video_href[0])
                    total_video_title.append(dir_name)
                    mp3_path = dir_path+'/'+dir_name+'/ulsan_'+dir_name+'.wav'
                    total_mp3_path.append(mp3_path)
        
        page_num = page_num + 1

        if '20101222' in total_video_title: break

    print("total_video_title : "+str(len(total_video_title)))
    print("total_video_href : "+str(len(total_video_href)))
    print("total_mp3_path : "+str(len(total_mp3_path)))
    # 회의록 href 및 회의록 진행 날짜 crawling

    text_page = 5
    for i in range(133, 221):
        if(i == 163 or i == 198): text_page = text_page + 1

        index2 = 0
        duplicate_count = 2

        url = base_url+str(text_page)+'&aCode=A&th='+str(i)+'&tag=cacha#postop'
        response = requests.get(url)
        # 회의록이 없는 경우 오류 방지
        if(response.status_code != 200): continue
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        href = [i.get("href") for i in soup.select('ul#late_skin li.minus li.minus li.minus li.minus a')]
        origin_title = [i.get_text() for i in soup.select('#late_skin > li.minus > ul > li.minus > ul > li.minus > ul > li > a')]
    
        for i in origin_title:
            title_text = only_num.sub('', i)
            while(len(title_text)!=8):
                title_text = title_text[1:]
            
            if title_text in total_text_title:
                title_text = title_text+'('+str(duplicate_count)+')'
                duplicate_count = duplicate_count + 1

            total_text_title.append(title_text)
            total_text_href.append(href[index2])
            index2 = index2 + 1

    print("텍스트 회의록 갯수 : "+str(len(total_text_href)))

    for video_title in total_video_title:
        if video_title not in total_text_title:
            lost_something.append(video_title)
    
    print("영상은 있지만 회의록이 없는 경우 : "+str(len(lost_something)))
    
    for text_title in total_text_title:
        if len(text_title) == 8:
            if text_title not in total_video_title:
                lost_something.append(text_title)
        else:
            if text_title[:-3] not in total_video_title:
                lost_something.append(text_title)
    print("영상 혹은 회의록이 없는 갯수 : "+str(len(lost_something)))

    # 날짜로 text_list index 값 찾을 수 있는지 test
    mp3_index = 0
    count = 0
    for video_title in total_video_title:
        if video_title in lost_something:
            mp3_index = mp3_index + 1
            continue
        index_text = total_text_title.index(video_title)

        count = count + 1
        mp3_index = mp3_index + 1
    print("영상 & 회의록이 있는 폴더 갯수(실제 생성한 폴더) : "+str(count))

# 울산 의회 운영위원회 동영상 mp4 url 가져오기 & 오디오 파일 추출
    if response.status_code == 200: plenary_download_audio_text(dir_path, total_video_title, lost_something, total_text_title, total_text_href, total_video_href, total_mp3_path)
    else: print(response.status_code)