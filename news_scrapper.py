from GoogleNews import GoogleNews
from src.database import Database
import time
import datetime
database = Database()

print(f'The news scrapper ran {datetime.datetime.now()}')
googlenews = GoogleNews(lang='en-PH', region='PH', period='3d')

candidates =[
    {"candidate": "Marcos-Duterte", "keyword":"marcos"},
    {"candidate": "Pacquiao-Atienza", "keyword":"pacquiao"},
    {"candidate": "Lacson-Sotto", "keyword":"lacson"},
    {"candidate": "Isko-Ong", "keyword":"moreno"},
    {"candidate": "Leni-Kiko", "keyword":"robredo"},
    {"candidate": "deguzman-bello", "keyword":"de guzman"},

]

for candidate in candidates:
    googlenews.clear()
    googlenews.get_news(candidate['keyword'])

    print(f"Scrapping {candidate['candidate']}")
    try:
        results=googlenews.results()
        for res in results:
            database.insert_news(title=res['title'],date=res['datetime'], link=res['link'], image=res['img'], site=res['site'], candidate=candidate['candidate'])
    except Exception as e:
        print(e)

    time.sleep(60)