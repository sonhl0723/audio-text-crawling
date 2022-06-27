# -*- coding: utf-8 -*-

from seoul.conf import *

def seoul_crawling():
    only_num = re.compile('[^0-9]') # 날짜 전처리

    for url_code in url_change:
        if os.path.isdir(base_url+mkdir_list[url_code]+"/"):
            if os.path.isdir(base_url+mkdir_list[url_code]+"/"+last_date_list[url_code]+"/seoul_"+last_date_list[url_code]+".txt"):
                print("Download Completely => "+mkdir_list[url_code])
                continue
        else: os.mkdir(base_url+mkdir_list[url_code]+"/")

        first_page_num_max = 10 # 대수구분
        break_flag = -1

        total_video_href = [] # mp4 url을 가져올 수 있는 href
        total_title = [] # 회의록 날짜
        same_date_count = {} # 날짜 중복 체크

        while(1):
            if break_flag == 1: break

            second_page_num = 1 # 페이지 number

            while(1):
                url = "https://ms.smc.seoul.kr/kr/cast/vod.do?sTh="+str(first_page_num_max)+"&session=&committeeCode="+url_code+"&startDay=&endDay=&flag=&keyword=&pageNum="+str(second_page_num)
                response = requests.get(url)
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                not_exist = soup.select_one('#sub_general > div.box1 > ul > li').get_text().strip()

                if second_page_num == 1 and not_exist =="조회된 목록이 없습니다.": # 더 이상 페이지가 존재하지 않을 경우
                    break_flag = 1
                    break
                elif not_exist =="조회된 목록이 없습니다.": break
                
                video_href = [i.get("data-key") for i in soup.select('div#sub_general div.box1 ul.depth1 li ul li a')]
                title = [i.get_text() for i in soup.select('div#sub_general div.box1 ul.depth1 li ul li a')]

                for i in title:
                    title_text = only_num.sub('', i)
                    while(len(title_text)!=8):
                        title_text = title_text[1:]
                    
                    try: same_date_count[title_text] += 1
                    except: same_date_count[title_text] = 1

                    if total_title.count(title_text) > 0:
                        title_text = title_text+"("+str(same_date_count[title_text])+")"
                        total_title.append(title_text)
                    else: total_title.append(title_text)
                
                for href in video_href: total_video_href.append(href)

                second_page_num = second_page_num + 1
                
            first_page_num_max = first_page_num_max - 1
            
        # 갯수 확인
        print(mkdir_list[url_code]+" : "+str(len(total_video_href)))
        print(mkdir_list[url_code]+" : "+str(len(total_title)))

        title_index = 0
        dir_path = base_url+mkdir_list[url_code]
        count = 0

        for href_code in total_video_href:
            url = "https://ms.smc.seoul.kr/cast/viewer/record.do?key="+href_code
            response = requests.get(url)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            video_text = soup.select_one('#record').get_text().strip()
            mp4_url = soup.select_one('#vod_wrap > div.wrap > div.content > div.cont_top.clx > div.vod_info > div.info_box.angun > div > a').get("href")
            wav_path = dir_path+"/"+total_title[title_index]+"/seoul_"+total_title[title_index]+".wav"
            text_path = dir_path + "/"+total_title[title_index]+"/seoul_"+total_title[title_index]+".txt"

            # 텍스트 회의록이 없을 경우
            if video_text == "회의록을 준비 중 입니다.":
                title_index = title_index + 1
                continue

            # 음성 파일 및 텍스트 회의록이 다운이 완료된 경우
            if os.path.isdir(dir_path+"/"+total_title[title_index]):
                if os.path.isfile(wav_path) and os.path.isfile(text_path):
                    title_index = title_index + 1
                    continue
            else: os.mkdir(dir_path+"/"+total_title[title_index]+"/")

            try: videoClip = VideoFileClip(mp4_url)
            except:
                print("mp4 url not exist")
                continue
            audioclip = videoClip.audio
            audioclip.write_audiofile(wav_path)
            audioclip.close()
            videoClip.close()

            Path(text_path).touch()
            text_file = open(text_path, "a")
            text_file.write(video_text)
            text_file.close()
            
            title_index = title_index + 1
            count = count + 1

        print(dir_path+" => real download : "+str(count))