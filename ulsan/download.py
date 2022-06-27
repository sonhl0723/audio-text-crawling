from ulsan.conf import *

def download_audio_text(index, total_video_title, lost_something, total_text_title, total_text_href, total_video_href, total_mp3_path):
    title_index = 0

    dir_path = base_path+mkdir_list[index]

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
            if i[-1] == '.' or i[-1] == ',': result = result + i[0:-1]
            elif i.isalnum() != False or i != '':
                for j in list(i): result = result + hangul.sub('', j)
        
        file_path = dir_path+"/"+str(total_text_title[index_text])+"/ulsan_"+str(total_text_title[index_text])+".txt"
        Path(file_path).touch()
        text_file = open(file_path, "a")
        text_file.write(result)
        text_file.close()

def plenary_download_audio_text(dir_path, total_video_title, lost_something, total_text_title, total_text_href, total_video_href, total_mp3_path):
    title_index = 0

    for video_title in total_video_title:
        duplicate_index_text = -1
        if video_title in lost_something:
            title_index = title_index + 1
            continue
        
        index_text = total_text_title.index(video_title)    # 회의록의 index에 접근하기 위한 value
        if video_title+"(2)" in total_text_title: duplicate_index_text = total_text_title.index(video_title+"(2)")

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

        if os.path.isfile(dir_path + "/" + video_title + '/ulsan_'+video_title+'.wav') and os.path.isfile(dir_path + "/" + video_title + '/ulsan_'+video_title+'.txt'):
            print("Pass => "+dir_path + "/" + video_title + "/")
            title_index = title_index + 1
            continue
        elif not os.path.isfile(dir_path + "/" + video_title + '/ulsan_'+video_title+'.txt'):
            try: videoClip = VideoFileClip(mp4_url)
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