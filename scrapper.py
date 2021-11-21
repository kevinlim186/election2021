from facebook_scraper import get_posts
from src.database import Database
from src.config import config,cookies
import http.cookiejar
import json


database = Database()
init_pages= 1000

groups_to_scrape =[
    {"id": 'groups/marcosdutertefor2022', "candidate": "Marcos-Duterte"},
    {"id": '1683989658430119', "candidate": "Isko"}
]

##convert string to cookiejar
cj = http.cookiejar.CookieJar()
cookies = json.loads(cookies)
for c in cookies:
     cookie = http.cookiejar.Cookie(
                version=0, name=c['name'], 
                value=c['value'], port=None, 
                port_specified=False, domain=c['domain'], 
                domain_specified=False, domain_initial_dot='', 
                path=c['path'], path_specified=False, 
                secure=c['secure'], expires=c['expirationDate'], 
                discard=False, comment=False, 
                comment_url='', rest='', rfc2109=True)

     cj.set_cookie(cookie)

for group in groups_to_scrape:
    for post in get_posts(group['id'], pages=init_pages,options={"comments": True},cookies=cj):
        print("Scrapping Group for {} with Post id {}".format(group['candidate'], post['post_id']))
        database.insert_post(
                post_id=post['post_id'],
                _text=post['text'],
                time_stamp=post['time'],
                likes=post['likes'],
                comments=post['comments'],
                shares=post['shares'],
                user_id=post['user_id'],
                username=post['username'],
                group_id=group['id'],
                group_candidate=group['candidate'])
        
        for comment in post['comments_full']:
            database.insert_comment(
                post_id=post['post_id'],
                comment_id=comment['comment_id'],
                _text=comment['comment_text'],
                time_stamp=comment['comment_time'],
                user_id=comment['commenter_id'],
                username=comment['commenter_name']
            )
