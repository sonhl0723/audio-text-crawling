from assembly.conf import *

def prep_text(target):
    only_character=re.compile('[^a-zA-Z0-9가-힣\s%]')
    flag=False
    if len(target)>1:
        if target[-1]=="." or target[-1]=="?" or target[-1]=="!": flag=True
    if target.find("(")!=-1 and target.find("(")!=(len(target)-1):
        if target[target.find("(")+1]!="임":
            start_point=target.find("(")
            end_point=target.find(")")
            new_text1=target[:start_point]
            new_text2=target[end_point:]
            target=new_text1+new_text2
        
    target=only_character.sub('',target)
    if flag: target=target+"\n"

    return target

def define_council(target):
    if target=="법사위": return "법제사법위원회"
    elif target=="정무위": return "정무위원회"
    elif target=="기재위": return "기획재정위원회"
    elif target=="교육위" or target=="교육위(17)": return "교육위원회"
    elif target=="과방위": return "과학기술정보방송통신위원회"
    elif target=="외통위": return "외교통일위원회"
    elif target=="국방위": return "국방위원회"
    elif target=="행안위": return "행정안전위원회"
    elif target=="문체위": return "문화체육관광위원회"
    elif target=="농해수위": return "농림축산식품해양수산위원회"
    elif target=="산자중기위": return "산업통상자원중소벤처기업위원회"
    elif target=="복지위": return "보건복지위원회"
    elif target=="환노위": return "환경노동위원회"
    elif target=="국토위": return "국토교통위원회"
    elif target=="정보위": return "정보위원회"
    elif target=="여가위": return "여성가족위원회"
    elif target=="특별위": return "특별위원회"
    elif target=="운영위": return "국회운영위원회"
    elif target=="미방위": return "미래창조과학방송통신위원회"
    elif target=="교문위": return "교육문화체육관광위원회"
    elif target=="안전행정위": return "안전행정위원회"
    elif target=="교과위": return "교육과학기술위원회"
    elif target=="외통위(19)": return "외교통상통일위원회"
    elif target=="지경위": return "지식경제위원회"
    elif target=="국토해양위": return "국토해양위원회"
    elif target=="복지가족위": return "보건복지가족위원회"
    elif target=="여성위": return "여성위원회"
    elif target=="문광위": return "문화관광위원회"
    elif target=="산자위": return "산업통상자원위원회"
    elif target=="산자위(17)": return "산업자원위원회"
    elif target=="재경위": return "재정경제위원회"
    elif target=="통외위": return "통일외교통상위원회"
    elif target=="농해위": return "농림해양수산위원회"
    elif target=="행자위": return "행정자치위원회"
    elif target=="문교공보위": return "문교공보위원회"
    elif target=="문화공보위": return "문화공보위원회"
    elif target=="외무위": return "외무통일위원회"
    elif target=="과정위": return "과학기술정보통신위원회"
    elif target=="건교위": return "건설교통위원회"
    elif target=="예결위": return "예산결산특별위원회"
    elif target=="농식품위": return "농림축산식품해양수산위원회"
    elif target=="문방위": return "문화체육관광방송통신위원회"
