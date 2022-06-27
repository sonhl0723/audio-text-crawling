from tvchosun.conf import *

def prep_text(target):
    result_text=""
    only_character=re.compile('[^a-zA-Z0-9가-힣\s%.]')

    for sent in target:
        if sent.find('[')!=-1 or sent.find(']')!=-1 or sent.find('/')!=-1:
                continue
        sent=sent.split(' ')
        for sent_elem in sent:
            flag=False
            if len(sent_elem)<1: continue
            elif sent_elem[0]=='.' or sent_elem[0]=='?' or sent_elem[0]=='!':
                result_text=result_text+'\n'
                continue
            flag=False
            start_parenthesis=sent_elem.find("(")
            end_parenthesis=sent_elem.find(")")

            if len(sent_elem)>=2:
                if sent_elem[-1]=='.' and sent_elem[-2].isdigit():
                    continue
                elif sent_elem[-1]=='?' or sent_elem[-1]=='!' or sent_elem[-1]=='.':
                    sent_elem=sent_elem[:-1]
                    flag=True
                elif sent_elem[-1]=='"' and sent_elem[-2]=='.':
                    sent_elem=sent_elem[:-2]
                    falg=True
                
                if start_parenthesis==0 and end_parenthesis==len(sent_elem)-1:
                    continue
                elif start_parenthesis!=-1 and end_parenthesis==-1:
                    sent_elem=sent_elem[:start_parenthesis]
                elif start_parenthesis==-1 and end_parenthesis!=-1:
                    sent_elem=sent_elem[end_parenthesis:]
                else:
                    newText1=sent_elem[:start_parenthesis]
                    newText2=sent_elem[end_parenthesis:]
                    sent_elem=newText1+newText2
                        
            sent_elem=only_character.sub('',sent_elem)

            if flag:
                result_text=result_text+sent_elem+'\n'
            else:
                result_text=result_text+sent_elem+' '

    return result_text


def wrong_date_check(url):
    s=requests.session()
    s.keep_alive=False
    response=s.get(url)
    if response.status_code == 200:
        html=response.text
        soup=BeautifulSoup(html, 'html.parser')

        try:
            check_item=soup.select_one("#iframe > div.popular_tag.mgt40 > h3").get_text()

            return True
        except AttributeError as e: return False
    else:
        print(response.status_code)
        return True