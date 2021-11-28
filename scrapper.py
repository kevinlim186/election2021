from facebook_scraper import get_posts,get_profile
from src.database import Database
from src.config import config,cookies
import http.cookiejar
import json
import time
from random import randrange
import sys


database = Database()
init_pages= 10
limit_user_scrape =1000

groups_to_scrape =[
#    {"id": 'BongbongMarcos', "candidate": "Marcos-Duterte"},
    {"id": 'groups/marcosdutertefor2022', "candidate": "Marcos-Duterte"},
    {"id": 'groups/777125892895858', "candidate": "Marcos-Duterte"},
    {"id": 'groups/976328462455714', "candidate": "Marcos-Duterte"},
    {"id": 'BanatBy', "candidate": "Marcos-Duterte"},
    
    {"id": 'VPLeniRobredoPH', "candidate": "Leni-Kiko"},
    {"id": 'groups/NOBS2016/', "candidate": "Leni-Kiko"},
    {"id": 'groups/945591229575374', "candidate": "Leni-Kiko"},
    {"id": 'groups/2556648484480195', "candidate": "Leni-Kiko"},

    {"id": 'iskomorenodomagoso', "candidate": "Isko-Ong"},
    {"id": 'groups/1683989658430119', "candidate": "Isko-Ong"},
    {"id": 'groups/997990110658082', "candidate": "Isko-Ong"},
    {"id": 'groups/174319694228563', "candidate": "Isko-Ong"},
    
    {"id": 'philstarnews', "candidate": "phil-star"},
    {"id": 'manilabulletin', "candidate": "manila-bullletin"},
    {"id": 'rappler', "candidate": "rapplerdotcom"},
]

def wait(time_remaining, message="Waiting to avoid scrapping guards"):
    for remaining in range(time_remaining, -1, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:s} :{:2d} secs".format(message, remaining))
        sys.stdout.flush()
        time.sleep(1)
    print('\n')

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
    try:
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
            
            #avoid to many request
            wait_time = randrange(30)
            wait(wait_time)
    except Exception as e:
        print("Problem with group {}".format(group['id']))
        print(e)


##user scrapping
users=database.get_all_user_with_post(limit=limit_user_scrape)
users=users.iloc[:limit_user_scrape]

known_keys=['Friend_count', 'Follower_count', 'Following_count', 'id', 'Name','Work', 'Places Lived','Life Events','Contact Info','Education', 'Basic Info','Relationship', 'Family Members', 'About', 'Friends'] 

for _,user in users.iterrows():
    try:
        profile = get_profile(str(user['user_id']), friends=10,cookies=cj)
    except Exception as e:
        wait(time_remaining=60, message="The account is blocked. Waiting for 1 minutes")
        break

    #to avoid missing key error
    json_keys = list(profile.keys())
    for key in known_keys:
        if key not in json_keys:
            profile[key]=None

    database.insert_user(
            user_id=int(profile['id']), 
            name=profile['Name'], 
            friend_count=profile['Friend_count'], 
            follower_count=profile['Follower_count'],
            following_count=profile['Following_count'], 
            work=str(profile['Work']), 
            places_lived=str(profile['Places Lived']), 
            life_events=str(profile['Life Events']),
            contact_inf=str(profile['Contact Info']),
            education=str(profile['Education']),
            basic_info=str(profile['Basic Info']),
            relationship=str(profile['Relationship']),
            family_member=str(profile['Family Members']),
            about=str(profile['About']),
        )

    if profile['Friends'] is not None:
        for friend in profile['Friends']:
            database.insert_connection(int(profile['id']),  int(friend['id']))

    #avoid to many request
    wait_time = randrange(30)
    wait(wait_time)


