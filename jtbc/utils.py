from jtbc.conf import *

def current_date_check():
    response = requests.get(conf_data['CURRENT_URL'])
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    return soup.select_one("#form1 > div.news_main > div.review_list > div.hd > h4").text.split(" ")[0].replace(".","")

def prep_text(target):
    result_text=""

    for sent in target:
        if sent[0]=='\n':
            continue
        elif sent[0]=="[" and sent.find(".")==-1:
            continue
        elif len(sent)>1 and sent[0].isdigit() and sent[1]==".":
            continue

        if sent[0]=="[" and sent.find(".")!=-1 and sent.find(":")!=-1:
            sent=sent.split(":")[1]
            sent=sent[:-1]

        sent=re.sub(r'\([^)]*\)', '', sent)
        index=sent.find(".")
        if index==-1:
            result_text=result_text+sent
        while index > -1:
            try:
                if index!=0 and index!=len(sent):
                    if not sent[index-1].isdigit():
                        result_text=result_text+sent[:index]+'\n'
                        sent=sent[index+1:]
                    else:
                        result_text=result_text+sent[:index+1]
                        sent=sent[index+2:]
                elif index==len(sent):
                    result_text=result_text+sent[:-1]+'\n'
                    sent=""
                elif index==0:
                    sent=sent[1:]

                index=sent.find(".")
            except ValueError:
                break

    return result_text