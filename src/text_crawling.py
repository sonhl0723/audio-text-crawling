# -*- coding: utf-8 -*-

import os
import requests
from bs4 import BeautifulSoup
import re
from pathlib import Path

def text_crawling():
    only_num = re.compile('[^0-9]')
    text_page = 5
    total_text_href = []
    total__text_title = []

    # 회의록 text의 href 및 날짜 title 얻어오기
    for i in range(129, 220):
        if i == 197 or i == 196 or i == 162:
            continue
        elif(i == 163 or i == 198):
            text_page = text_page + 1
        index = 0
        url = 'https://www.council.ulsan.kr/minutes/assembly/search/simple1.html?daesu='+str(text_page)+'&aCode=C&cCode=C101&th='+str(i)+'&tag=cccha#postop'
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        href = [i.get("href") for i in soup.select('ul#late_skin li.minus li.minus li.minus li.minus li.minus a')]
        title = [i.get_text() for i in soup.select('#late_skin > li.minus > ul > li.minus > ul > li.minus > ul > li.minus > ul > li > a')]
        for i in title:
            title_text = only_num.sub('', i)
            if len(title_text) != 8:
                title_text = title_text[1:]
            
            total_text_title.append(title_text)
            total_text_href.append(href[index])
            index = index + 1
    # 확인 코드
    print("href 총 갯수 : "+str(len(total__text_href))+"   href 형식"+str(total_text_href[0]))
    print("title 총 갯수 : "+str(len(total_text_title))+"   title 형식"+str(total_text_title[0]))
            
    # text url 접근 후 text 파일 생성
    index = 0   # total_text_title index값
    count = 0   # 생성한 회의록 수

    dir_path = './data'
    for href in total_text_href:
        url = 'https://www.council.ulsan.kr/' + href
        response = requests.get(url)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        # hangul = re.compile('[^ 0-9ㄱ-ㅣ가-힣]+')
        hangul = re.compile('[^0-9가-힣]')
        str_soup = str(soup).split()
        result = ""
        for i in str_soup:
            if i[-1] == '.' or i[-1] == ',':
                result = result + i[0:-1]
            elif i.isalnum() != False or i != '':
                for j in list(i):
                    result = result + hangul.sub('', j)


        file_path = dir_path+"/"+str(total_text_title[index])+"/"+str(total_text_title[index])+".txt"

        if Path(dir_path+"/"+str(total_text_title[index])).exists():
            Path(file_path).touch()
            text_file = open(file_path, "a")
            text_file.write(result)
            text_file.close()
            index = index + 1
            count = count + 1
        elif str(total_text_title[index]) == '20130611':
            file_path = dir_path+"/20130612/20130612.txt"
            Path(file_path).touch()
            index = index + 1
            count = count + 1
        else:
            print(file_path)    # 오디오 파일이 없는 회의록
            index = index + 1
            continue
    
    print("생성한 회의록 수 : "  + str(count))    # 생성한 회의록 수


text_crawling()