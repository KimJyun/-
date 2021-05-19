#json 파일이 사람마다 달라서 확인필요

# import : firebase db
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# import : crowling
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import warnings

# import : make random key
import random
import string

# db
cred = credentials.Certificate("crowlingtest-firebase-adminsdk-566vk-c23534af09.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://crowlingtest.firebaseio.com/"})

# crowling
currPage = 1
endPage = 1
countContents = 0
goto = 1 # 1 : true, 0 : false

while True:
    goto = 1
    dir = db.reference("검색어")
    keyword = dir.get()
    keyword = keyword.replace('"','')
    print(keyword)
    if(keyword == "종료"):
        break
    
    baseUrl = "https://search.naver.com/search.naver?query="
    plusUrl = keyword


    while currPage == endPage:
        
        url = baseUrl + urllib.parse.quote_plus(plusUrl) + "&sm=tab_pge&srchby=all&st=sim&where=post&start=" + str(currPage)

        html = urllib.request.urlopen(url).read()
        soupSearch = BeautifulSoup(html, "html.parser")
        contents = soupSearch.find_all('a', {"class": "api_txt_lines total_tit"})

        dir = db.reference(plusUrl)  # 검색어 하위에 데이터베이스 생성


        for i in contents:

            if (countContents >= 10 or goto == 0):
                break

            # init "value"
            save_title = i.text             # 블로그 제목 > get title
            save_url = i.attrs['href']      # 블로그 url > get url
            blogBody = ""                   # 블로그 본문
            score = 0                       # 광고성 점수
            agree = 0
            disagree = 0

            # 본문
            warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

            blogUrl = urllib.request.urlopen(save_url).read()
            soupBlog = BeautifulSoup(blogUrl, "html.parser")
            body = soupBlog.select("#mainFrame")

            
            if "blog.naver.com" in save_url:
                if len(body) > 0:
                    contentUrl = urllib.request.urlopen("https://blog.naver.com" + body[0]['src']).read()
                    soupContent = BeautifulSoup(contentUrl, "html.parser")
                    components = soupContent.select(".se-main-container .se-component")

                    for component in components:
                        blogBody += component.text.strip("\n")

                    # check 광고성 여부
                    bad = ['경제적', '소정', '제공', '협찬', '유료', '대가성', "지원", "원고료", "업체", "제공받아", "식사권", "광고주", "해당업체", "무상", "작성되었습니다"]
                    good = ["내돈내산", "결제", "솔직후기", "영수증",  "찐후기", "실제리뷰"]
                    reverse = ["없", "않"]
        
                    for badWord in bad:
                        if badWord in blogBody:
                            score -= 1
                                            
                    for goodWord in good:
                        if goodWord in blogBody:
                            score += 1
                                
                    for badWord in bad:
                        for reverseWord in reverse:
                            if badWord + ' ' + reverseWord in blogBody:
                                score += 2
                            elif badWord + reverseWord in blogBody:
                                score += 2
                                                        
                    for goodWord in good:
                        for reverseWord in reverse:
                            if goodWord + ' ' + reverseWord in blogBody:
                                score -= 2
                            elif goodWord + reverseWord in blogBody:
                                score -= 2

                    # for check
                    print(save_title)
                    print(save_url)
                    print(blogBody)

                    # blog 글 일때만 db에 update
                    if blogBody:
                        urlKey = ''.join(e for e in save_url if e.isalnum())
                        urlKey = urlKey.replace("httpsblognavercom","")
                        overlap = 0
                        try:
                            for i in dir.get():
                                if i == urlKey:
                                    overlap = 1
                        except:
                            overlap = 0

                        if (overlap == 0):
                            dir.update({urlKey : [save_title, save_url, blogBody, score, agree, disagree, [""], [""]]})

                    dir = db.reference("검색어")
                    new_keyword = dir.get()
                    new_keyword = new_keyword.replace('"','')
                    if (keyword != new_keyword):
                            goto = 0
                    dir = db.reference(plusUrl)

            # go to the next page
            countContents += 1

        countContents = 0
        currPage += 1

    currPage = 1
        
    dir = db.reference("검색어")

    if (goto == 1):
        print("새로운 검색어를 기다리고 있습니다.....")
        while True:
            new_keyword = dir.get()
            new_keyword = new_keyword.replace('"','')
            if(keyword != new_keyword):
                print("검색어가 변경되었습니다.")
                break

    else:
        print("검색어가 변경되었습니다.")
