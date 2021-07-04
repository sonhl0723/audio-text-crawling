# -*- coding: utf-8 -*-

import ulsan
import seoul
import national

def select(num):
    if num == 0:
        print("Closing......")
        return exit()
    else:
        print(" ))))    Crawling start ==> "+select_list[int(select_num)], end="\n\n")
        print("Loading......")

    if num == 1:
        ulsan.plenary_meeting()
        return ulsan.ulsan_crawling()
    elif num == 2:
        return seoul.seoul_crawling()
    elif num == 3:
        return national.main()

select_list = {
    0 : "exit",
    1 : "ulsan",
    2 : "seoul",
    3 : "national assembly",
}

while(1):

    # Show List
    print("++++++++++   LIST    ++++++++++")
    for key, value in select_list.items():
        print(" ",key, ":",value)

    print("+++++++++++++++++++++++++++++++")


    try:    # 숫자 입력 시
        select_num = input("Choose an organization to crawl : ")
        # print(" ))))    Crawling start ==> "+select_list[int(select_num)], end="\n\n")
        select_list[int(select_num)]

    except Exception as e:  # 의회 이름 입력 시

        try:
            reverse_select_list = dict(map(reversed, select_list.items()))
            select_num = reverse_select_list[select_num]
            # print(" ))))    Crawling start ==> "+select_list[int(select_num)], end="\n\n")

        except Exception as e:  # 목록에 없는 숫자, 의회 이름 입력 시
            print("----Please select again----", end="\n\n")
            continue


    select_num = int(select_num)
    select(select_num)