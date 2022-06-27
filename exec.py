# -*- coding: utf-8 -*-

import ulsan.ulsan as ulsan
import ulsan.plenary as ulsan_p
import seoul.seoul as seoul
import assembly.national as national
import assembly.national_sub as national_sub
import jtbc.jtbc as jtbc
import tvchosun.tvcs as tvcs

def select(num):
    if num == 0:
        print("\tClosing......")
        return exit()
    else:
        print("\t ))))    Crawling start ==> "+select_list[int(select_num)], end="\n\n")
        print("\tLoading......")

    if num == 1:
        ulsan.ulsan_crawling()
        return ulsan_p.plenary_meeting()
    elif num == 2: return seoul.seoul_crawling()
    elif num == 3: return national.main()
    elif num == 4: return national_sub.main()
    elif num == 5: return jtbc.jtbc()
    elif num == 6: return tvcs.main()

select_list = {
    0 : "exit",
    1 : "ulsan",
    2 : "seoul",
    3 : "national assembly-only text",
    4 : "national assembly(ph/ch/igo)-only text",
    5 : "jtbc",
    6 : "TV Chosun-news9/news7",
}


if __name__=='__main__':
    print("\n\n")

    while(1):
        # Show List
        print("\t+++++++++++++++++++++++++   LIST    +++++++++++++++++++++++++")
        for key, value in select_list.items():
            print('\t',key, ":",value)

        print("\t+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("\n\n")


        try:    # 숫자 입력 시
            select_num = input("\tChoose an organization to crawl : ")
            # print(" ))))    Crawling start ==> "+select_list[int(select_num)], end="\n\n")
            select_list[int(select_num)]

        except Exception as e:  # 의회 이름 입력 시

            try:
                reverse_select_list = dict(map(reversed, select_list.items()))
                select_num = reverse_select_list[select_num]
                # print(" ))))    Crawling start ==> "+select_list[int(select_num)], end="\n\n")

            except Exception as e:  # 목록에 없는 숫자, 의회 이름 입력 시
                print("\t----Please select again----", end="\n\n")
                continue


        select_num = int(select_num)
        select(select_num)