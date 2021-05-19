import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver


# Firebase database 인증 및 앱 초기화
cred = credentials.Certificate('practice-84111-firebase-adminsdk-ywedg-722efc05f7.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://practice-84111.firebaseio.com/'})

url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EC%98%81%ED%86%B5+%EB%A7%9B%EC%A7%91"
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, "html.parser")
contents = soup.find_all('a',{'class': 'api_txt_lines total_tit'})

dir = db.reference()

for i in contents:
    save_title = i.text
    print(save_title)

    save_url = i.attrs['href']
    print(save_url)

    dir.update({save_title : save_url})
