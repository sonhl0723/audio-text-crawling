# -*- coding: utf-8 -*-

# import sys
# import os
# sys.path.append(os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ))

from ulsan.conf import *
from ulsan.download import download_audio_text

def ulsan_crawling():
    only_num = re.compile('[^0-9]') # 날짜 전처리

    for index in range(len(text_url_change)):
        if os.path.isdir(base_path+mkdir_list[index]+"/"):
            if os.path.isdir(base_path+mkdir_list[index]+"/"+last_date_list[index]+"/ulsan_"+last_date_list[index]+".txt"):
                print("Download Completely => "+mkdir_list[index])
                continue
        else: os.mkdir(base_path+mkdir_list[index]+"/")

        url = select_council_url+text_url_change[index]
        response = requests.get(url)

        video_page = 1
        text_page = text_page_list[index]

        total_text_href = []    # 회의록 href list
        total_text_title = []   # 회의록 날짜  list
        total_video_href = []   # 영상회의록 href list
        total_video_title = []  # 영상회의록 날짜 list
        total_mp3_path = []     # 영상회의록 저장 path list
        lost_something = []     # 회의록 or 영상회의록 없는 날짜 list

        if response.status_code == 200:
            while(1):           # total_video_href & total_video_title & total_mp3_path
                video_page = video_page + 1
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                video_href = [i.get("href") for i in soup.select('td.data a')]
                for href in video_href:
                    if href in break_href_list:
                        break
                    total_video_href.append(href)
                dir_path = base_path+mkdir_list[index]

                break_flag = 0

                for i in range(len(video_href)):
                    if break_flag == 1:
                        break
                    dir_name = soup.select_one('#divContents > div > section > div > form > div:nth-child(9) > table > tbody > tr:nth-child('+ str(i+1) +') > td:nth-child(4)').get_text().strip()
                    dir_name = only_num.sub('', dir_name)

                    if(dir_name == last_date_list[index]): break_flag = 1

                    total_video_title.append(dir_name)
                    mp3_path = dir_path+'/'+dir_name+'/ulsan_'+dir_name+'.wav'
                    total_mp3_path.append(mp3_path)
                if break_flag == 1: break
                url = select_council_url+text_url_change[index]+'&pageIndex='+str(video_page)
                response = requests.get(url)

            print("영상 회의록 갯수 : " + str(len(total_video_href)))

            # 회의록 href 및 회의록 진행 날짜 crawling
            for i in range(text_range_list[index][0], text_range_list[index][1]):
                if(i == 163 or i == 198): text_page = text_page + 1

                index2 = 0

                if text_url_change[index][0] == 'C': url = base_url+str(text_page)+'&aCode=C&cCode='+text_url_change[index]+'&th='+str(i)+'&tag=cccha#postop'
                elif text_url_change[index][0] == 'E':
                    if text_url_change[index][3] == '1': url = base_url+str(text_page)+'&aCode='+text_url_change[index]+'&th='+str(i)+'&tag=cacha#postop'
                    elif text_url_change[index][3] == '7': url = base_url+str(text_page)+'&aCode=G&gCode=G735&th='+str(i)+'&tag=cacha#postop'
                    elif text_url_change[index][3] == '8': url = base_url+str(text_page)+'&aCode=G&gCode=G730&th='+str(i)+'&tag=cacha#postop'
                    elif text_url_change[index][3] == '5': url = base_url+str(text_page)+'&aCode=G&gCode=G710&th='+str(i)+'&tag=cacha#postop'
                    elif text_url_change[index][3] == '9': url = base_url+str(text_page)+'&aCode=G&gCode=G720&th='+str(i)+'&tag=cacha#postop'
                    else: url = base_url+str(text_page)+'&aCode=G&gCode=G'+text_url_change[index][1:]+'&th='+str(i)+'&tag=cgcha#postop'
                response = requests.get(url)
                # 회의록이 없는 경우 오류 방지
                if(response.status_code != 200):
                    continue
                
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')

                if text_url_change[index][0] == 'C':
                    href = [i.get("href") for i in soup.select('ul#late_skin li.minus li.minus li.minus li.minus li.minus a')]
                    title = [i.get_text() for i in soup.select('#late_skin > li.minus > ul > li.minus > ul > li.minus > ul > li.minus > ul > li > a')]
                elif text_url_change[index][0] == 'E':
                    if text_url_change[index][3] == '1':
                        href = [i.get("href") for i in soup.select('ul#late_skin li.minus li.minus li.minus li.minus a')]
                        title = [i.get_text() for i in soup.select('#late_skin > li.minus > ul > li.minus > ul > li.minus > ul > li > a')]
                    else:
                        href = [i.get("href") for i in soup.select('ul#late_skin li li li li.minus a')]
                        title = [i.get_text() for i in soup.select('#late_skin > li > ul > li > ul > li > ul > li.minus > a')]

                for i in title:
                    title_text = only_num.sub('', i)
                    while(len(title_text)!=8):
                        title_text = title_text[1:]
                    
                    total_text_title.append(title_text)
                    total_text_href.append(href[index2])
                    index2 = index2 + 1
            # 확인 코드
            print("텍스트 회의록 갯수 : "+str(len(total_text_href)))

            # 영상회의록 및 회의록 비교 후 매치 실패된 회의록 판별
            for video_title in total_video_title:
                if video_title not in total_text_title: lost_something.append(video_title)
            
            print("영상은 있지만 회의록이 없는 경우 : "+str(len(lost_something)))
            
            for text_title in total_text_title:
                if text_title not in total_video_title:
                    lost_something.append(text_title)
            print("영상 혹은 회의록이 없는 갯수 : "+str(len(lost_something)))

            # 날짜로 text_list index 값 찾을 수 있는지 test
            mp3_index = 0
            count = 0
            for video_title in total_video_title:
                if video_title in lost_something:
                    mp3_index = mp3_index + 1
                    continue

                count = count + 1
                mp3_index = mp3_index + 1
            print("영상 & 회의록이 있는 폴더 갯수(실제 생성한 폴더) : "+str(count))
        else: print(response.status_code)

        if response.status_code == 200: download_audio_text(index, total_video_title, lost_something, total_text_title, total_text_href, total_video_href, total_mp3_path)
        else: print(response.status_code)