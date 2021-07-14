# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import os
from pathlib import Path
import re
from moviepy.editor import *

def ulsan_crawling():
# 울산 의회 운영위원회 동영상 href 및 제목 가져오기
    text_page_list = [5, 5, 5, 5, 5, 5, 7, 7, 7, 7, 7]
    break_href_list = ['/cast/viewVod.do?vod=732&bt=E',
    '/cast/viewVod.do?vod=1087&bt=E',
    '/cast/viewVod.do?vod=1096&bt=E',
    '/cast/viewVod.do?vod=1094&bt=E',
    '/cast/viewVod.do?vod=1098&bt=E'] # 다운로드 받지 않을 시작 href
    last_date_list = ['20100715', '20110210', '20110210', '20110210', '20110210', '20110511', '20181210', '20200826', '20200910', '20190718', '20210312'] # 다운받을 마지막 날짜
    text_range_list = [[129, 221], [134, 221], [134, 221], [134, 221], [134, 221], [137, 220], [201, 213], [215, 220], [216, 217], [206, 218], [220, 221]] # 회의록 범위
    text_url_change = ['C101', 'C601', 'C701', 'C501', 'C801', 'E011', 'E014', 'E017', 'E018', 'E015', 'E019']
    mkdir_list = ['council_operation', 'administration', 'environment', 'industry', 'education', 'budget', 'energy', 'young', 'economy', 'confirmation', 'nuclear']

    only_num = re.compile('[^0-9]') # 날짜 전처리

    for index in range(len(text_url_change)):
        if os.path.isdir("./data/ulsan/"+mkdir_list[index]+"/"):
            if os.path.isdir("./data/ulsan/"+mkdir_list[index]+"/"+last_date_list[index]+"/ulsan_"+last_date_list[index]+".txt"):
                print("Download Completely => "+mkdir_list[index])
                continue
        else:
            os.mkdir("./data/ulsan/"+mkdir_list[index]+"/")

        url = 'http://www.council.ulsan.kr/cast/sub/list.do?bbsId=castActivityVod&commCode='+text_url_change[index]
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
                dir_path = "./data/ulsan/"+mkdir_list[index]

                breaker = 0

                for i in range(len(video_href)):
                    if breaker == 1:
                        break
                    dir_name = soup.select_one('#divContents > div > section > div > form > div:nth-child(9) > table > tbody > tr:nth-child('+ str(i+1) +') > td:nth-child(4)').get_text().strip()
                    dir_name = only_num.sub('', dir_name)
                    if(dir_name == last_date_list[index]):
                        breaker = 1
                    total_video_title.append(dir_name)
                    mp3_path = dir_path+'/'+dir_name+'/ulsan_'+dir_name+'.wav'
                    total_mp3_path.append(mp3_path)
                if breaker == 1:
                    break
                url = 'http://www.council.ulsan.kr/cast/sub/list.do?bbsId=castActivityVod&commCode='+text_url_change[index]+'&pageIndex='+str(video_page)
                response = requests.get(url)
            # print("mp3_path 갯수 : " + str(len(total_mp3_path)))
            print("영상 회의록 갯수 : " + str(len(total_video_href)))
            # print("영상 회의록 title 갯수 : " + str(len(total_video_title)))

            # 회의록 href 및 회의록 진행 날짜 crawling
            for i in range(text_range_list[index][0], text_range_list[index][1]):
                if(i == 163 or i == 198):             # crawling url이 바뀌는 회의록 체크
                    text_page = text_page + 1
                index2 = 0
                if text_url_change[index][0] == 'C':
                    url = 'https://www.council.ulsan.kr/minutes/assembly/search/simple1.html?daesu='+str(text_page)+'&aCode=C&cCode='+text_url_change[index]+'&th='+str(i)+'&tag=cccha#postop'
                elif text_url_change[index][0] == 'E':
                    if text_url_change[index][3] == '1':
                        url = 'https://www.council.ulsan.kr/minutes/assembly/search/simple1.html?daesu='+str(text_page)+'&aCode='+text_url_change[index]+'&th='+str(i)+'&tag=cacha#postop'
                    elif text_url_change[index][3] == '7':
                        url = 'https://www.council.ulsan.kr/minutes/assembly/search/simple1.html?daesu='+str(text_page)+'&aCode=G&gCode=G735&th='+str(i)+'&tag=cacha#postop'
                    elif text_url_change[index][3] == '8':
                        url = 'https://www.council.ulsan.kr/minutes/assembly/search/simple1.html?daesu='+str(text_page)+'&aCode=G&gCode=G730&th='+str(i)+'&tag=cacha#postop'
                    elif text_url_change[index][3] == '5':
                        url = 'https://www.council.ulsan.kr/minutes/assembly/search/simple1.html?daesu='+str(text_page)+'&aCode=G&gCode=G710&th='+str(i)+'&tag=cacha#postop'
                    elif text_url_change[index][3] == '9':
                        url = 'https://www.council.ulsan.kr/minutes/assembly/search/simple1.html?daesu='+str(text_page)+'&aCode=G&gCode=G720&th='+str(i)+'&tag=cacha#postop'
                    else:
                        url = 'https://www.council.ulsan.kr/minutes/assembly/search/simple1.html?daesu='+str(text_page)+'&aCode=G&gCode=G'+text_url_change[index][1:]+'&th='+str(i)+'&tag=cgcha#postop'
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
                if video_title not in total_text_title:
                    lost_something.append(video_title)
            
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
                index_text = total_text_title.index(video_title)

                # print("video_title : "+video_title)
                # print("video_href : "+total_video_href[mp3_index])
                # print("text_title : "+total_text_title[index_text]+"    text_href : "+total_text_href[index_text])
                # print("mp3_path : "+total_mp3_path[mp3_index])
                count = count + 1
                mp3_index = mp3_index + 1
            print("영상 & 회의록이 있는 폴더 갯수(실제 생성한 폴더) : "+str(count))
        else:
            print(response.status_code)



    # 울산 의회 운영위원회 동영상 mp4 url 가져오기 & 오디오 파일 추출
        if response.status_code == 200:

            title_index = 0
            total_download = 0

            dir_path = "./data/ulsan/"+mkdir_list[index]

            for video_title in total_video_title:
                if video_title in lost_something:
                    title_index = title_index + 1
                    continue
                
                index_text = total_text_title.index(video_title)    # 회의록의 index에 접근하기 위한 value

                if not os.path.isdir(dir_path + "/" + video_title + "/"):
                    print("Create => "+dir_path + "/" + video_title + "/")
                    os.mkdir(dir_path + "/" + video_title + "/")

                video_url = 'https://www.council.ulsan.kr' + total_video_href[title_index]
                response = requests.get(video_url)
                mp3_path = total_mp3_path[title_index]

                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                str_1 = str(soup.find_all("script")).split()
                for i in str_1:
                    if "http" in i:
                        mp4_url = i[1:-2]

                if os.path.isfile(dir_path + "/" + video_title + '/ulsan_'+video_title+'.wav') and os.path.isfile(dir_path + "/" + video_title + '/ulsan_'+video_title+'.txt'):
                    print("Pass => "+dir_path + "/" + video_title + "/")
                    title_index = title_index + 1
                    continue
                elif not os.path.isfile(dir_path + "/" + video_title + '/ulsan_'+video_title+'.txt'):
                    try:
                        videoClip = VideoFileClip(mp4_url)
                    except:
                        print("mp4 url not exist")
                        continue
                    audioclip = videoClip.audio
                    audioclip.write_audiofile(mp3_path)
                    audioclip.close()
                    videoClip.close()

                title_index = title_index + 1

                text_url = 'https://www.council.ulsan.kr/' + total_text_href[index_text]
                response = requests.get(text_url)
                content = response.content
                soup = BeautifulSoup(content, 'html.parser')
                hangul = re.compile('[^0-9가-힣]')
                str_soup = str(soup).split()
                result = ""
                for i in str_soup:
                    if i[-1] == '.' or i[-1] == ',':
                        result = result + i[0:-1]
                    elif i.isalnum() != False or i != '':
                        for j in list(i):
                            result = result + hangul.sub('', j)
                
                file_path = dir_path+"/"+str(total_text_title[index_text])+"/ulsan_"+str(total_text_title[index_text])+".txt"
                Path(file_path).touch()
                text_file = open(file_path, "a")
                text_file.write(result)
                text_file.close()
                
        else:
            print(response.status_code)

# 본 회의 크롤링 실행 함수
def plenary_meeting():

    only_num = re.compile('[^0-9]') # 날짜 전처리

    page_num = 1

    if os.path.isdir("./data/ulsan/plenary meeting"):
        if os.path.isfile("./data/ulsan/plenary meeting/20101112/ulsan_20101112.txt"):
            print("Download Completely => plenary meeting")
            return 0
    else:
        os.mkdir("./data/ulsan/plenary meeting/")

    dir_path = "./data/ulsan/plenary meeting"

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
        if '20101222' in total_video_title:
            break
    print("total_video_title : "+str(len(total_video_title)))
    print("total_video_href : "+str(len(total_video_href)))
    print("total_mp3_path : "+str(len(total_mp3_path)))
    # 회의록 href 및 회의록 진행 날짜 crawling

    text_page = 5
    for i in range(133, 221):
        if(i == 163 or i == 198):             # crawling url이 바뀌는 회의록 체크
            text_page = text_page + 1

        index2 = 0
        duplicate_count = 2
        url = 'https://www.council.ulsan.kr/minutes/assembly/search/simple1.html?daesu='+str(text_page)+'&aCode=A&th='+str(i)+'&tag=cacha#postop'
        response = requests.get(url)
        # 회의록이 없는 경우 오류 방지
        if(response.status_code != 200):
            continue
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

        # print("video_title : "+video_title)
        # print("video_href : "+total_video_href[mp3_index])
        # print("text_title : "+total_text_title[index_text]+"    text_href : "+total_text_href[index_text])
        # print("mp3_path : "+total_mp3_path[mp3_index])
        count = count + 1
        mp3_index = mp3_index + 1
        # print("\n")
    print("영상 & 회의록이 있는 폴더 갯수(실제 생성한 폴더) : "+str(count))
    # print(total_text_title)

# 울산 의회 운영위원회 동영상 mp4 url 가져오기 & 오디오 파일 추출
    if response.status_code == 200:

        title_index = 0
        total_download = 0

        for video_title in total_video_title:
            duplicate_index_text = -1
            if video_title in lost_something:
                title_index = title_index + 1
                continue
            
            index_text = total_text_title.index(video_title)    # 회의록의 index에 접근하기 위한 value
            if video_title+"(2)" in total_text_title:
                duplicate_index_text = total_text_title.index(video_title+"(2)")

            if not os.path.isdir(dir_path + "/" + video_title + "/"):
                print("Create => "+dir_path + "/" + video_title + "/")
                os.mkdir(dir_path + "/" + video_title + "/")

            video_url = 'https://www.council.ulsan.kr' + total_video_href[title_index]
            response = requests.get(video_url)
            mp3_path = total_mp3_path[title_index]

            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            mp4_url = [i.get("src") for i in soup.select('#wndwVod')]
            mp4_url = 'https://www.council.ulsan.kr'+mp4_url[0]
            print(mp4_url)

            if os.path.isfile(dir_path + "/" + video_title + '/ulsan_'+video_title+'.wav') and os.path.isfile(dir_path + "/" + video_title + '/ulsan_'+video_title+'.txt'):
                print("Pass => "+dir_path + "/" + video_title + "/")
                title_index = title_index + 1
                continue
            elif not os.path.isfile(dir_path + "/" + video_title + '/ulsan_'+video_title+'.txt'):
                try:
                    videoClip = VideoFileClip(mp4_url)
                except:
                    print("mp4 url not exist")
                    continue
                audioclip = videoClip.audio
                audioclip.write_audiofile(mp3_path)
                audioclip.close()
                videoClip.close()

            title_index = title_index + 1

            text_url = 'https://www.council.ulsan.kr/' + total_text_href[index_text]
            response = requests.get(text_url)
            content = response.content
            soup = BeautifulSoup(content, 'html.parser')
            hangul = re.compile('[^0-9가-힣]')
            str_soup = str(soup).split()
            result = ""
            for i in str_soup:
                if i[-1] == '.' or i[-1] == ',':
                    result = result + i[0:-1]
                elif i.isalnum() != False or i != '':
                    for j in list(i):
                        result = result + hangul.sub('', j)
            
            file_path = dir_path+"/"+str(total_text_title[index_text])+"/ulsan_"+str(total_text_title[index_text])+".txt"
            Path(file_path).touch()
            text_file = open(file_path, "a")
            text_file.write(result)
            text_file.close()

            if not duplicate_index_text == -1:
                text_url = 'https://www.council.ulsan.kr/' + total_text_href[duplicate_index_text]
                response = requests.get(text_url)
                content = response.content
                soup = BeautifulSoup(content, 'html.parser')
                hangul = re.compile('[^0-9가-힣]')
                str_soup = str(soup).split()
                result = ""
                for i in str_soup:
                    if i[-1] == '.' or i[-1] == ',':
                        result = result + i[0:-1]
                    elif i.isalnum() != False or i != '':
                        for j in list(i):
                            result = result + hangul.sub('', j)
                
                file_path = dir_path+"/"+str(total_text_title[duplicate_index_text][:-3])+"/ulsan_"+str(total_text_title[duplicate_index_text])+".txt"
                Path(file_path).touch()
                text_file = open(file_path, "a")
                text_file.write(result)
                text_file.close()
            
    else:
        print(response.status_code)
    # print("total_video_href : "+str(len(total_video_href)))
    # print("total_video_title : "+str(len(total_video_title)))
    # print("total_mp3_path : "+str(len(total_mp3_path)))