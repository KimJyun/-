import urllib.request
import json


def search(key):
    #아이디와 비번
    client_id = "wpBS1Rz6eJEFJZ27x_SJ"
    client_secret = "p5fE_LZeNA"

    #url
    url_ori = "https://openapi.naver.com/v1/search/blog?query="
    url_sub = "&display=10&sort=date"
    url = url_ori + urllib.parse.quote(key) + url_sub # json 결과

    #api 검색 개체 - 헤더에 아이디 비번 추가
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)

    # 검색요청
    response = urllib.request.urlopen(request)
    rescode = response.getcode()


    if(rescode==200):
        return response.read().decode('utf-8')
    else:
        print("Error Code:" + rescode)



def ver(item):
    print("블로그 : " + item['title'])
    print("블로거 : " + item['bloggername'])
    print("요약 : " + item['description'])
    print("날짜 : " + item['postdate'])
    print("링크 : " + item['link'])
    print("------------------------------------------------------------------------")


def main():
    res= search(input("검색어를 입력하세요  :  "))

    if (res == None):
        print("검색에 실패하였습니다.")
        exit()

    jres = json.loads(res)
    for post in jres['items']:
        ver(post)

    if (jres == None):
        print("json.loads 실패하였습니다.")
        exit()

if __name__ == '__main__':
    main()