import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Firebase database 인증 및 앱 초기화
cred = credentials.Certificate('practice-84111-firebase-adminsdk-ywedg-722efc05f7.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://practice-84111.firebaseio.com/'
})

dir = db.reference('Memo')  # 기본 위치 지정
dir.update({'TestTag': '기아'}) # 수정



