from facebook_scraper import get_posts,get_profile
from src.database import Database
from src.config import config,cookies
import http.cookiejar
import json
import time
from random import randrange
import sys
import datetime

database = Database()
init_pages= 20
limit_user_scrape =1000

groups_to_scrape =[
    {"id": 'groups/297928491680206', "candidate": "Pacquiao-Atienza"},
    {"id": 'groups/787502051653675', "candidate": "Pacquiao-Atienza"},
    {"id": 'groups/3366074970143394', "candidate": "Pacquiao-Atienza"},
    {"id": 'groups/officialmannypacquiaosupporters', "candidate": "Pacquiao-Atienza"},
    {"id": 'MannyPacquiao', "candidate": "Pacquiao-Atienza"},
    {"id": 'groups/553549955633620', "candidate": "Pacquiao-Atienza"},
    {"id": 'groups/531471551246993', "candidate": "Pacquiao-Atienza"},

    {"id": 'PingLacsonOfficial', "candidate": "Lacson-Sotto"},
    {"id": 'groups/190638622594926', "candidate": "Lacson-Sotto"},
    {"id": 'groups/270131633191090', "candidate": "Lacson-Sotto"},
    {"id": 'groups/1614639185418385', "candidate": "Lacson-Sotto"},
    {"id": 'groups/pinglacsontitosotto', "candidate": "Lacson-Sotto"},
    {"id": 'groups/teamlacsonsotto', "candidate": "Lacson-Sotto"},
    {"id": 'pinglacsonkami', "candidate": "Lacson-Sotto"},


#    {"id": 'BongbongMarcos', "candidate": "Marcos-Duterte"},
    {"id": 'groups/marcosdutertefor2022', "candidate": "Marcos-Duterte"},
    {"id": 'groups/777125892895858', "candidate": "Marcos-Duterte"},
    {"id": 'groups/976328462455714', "candidate": "Marcos-Duterte"},
    {"id": 'groups/463316131033015', "candidate": "Marcos-Duterte"},
    {"id": 'groups/321991487837550', "candidate": "Marcos-Duterte"},
    {"id": 'groups/204653531230918', "candidate": "Marcos-Duterte"},
    {"id": 'groups/BongbongMarcosForPresident2022', "candidate": "Marcos-Duterte"},
    
    
    {"id": 'VPLeniRobredoPH', "candidate": "Leni-Kiko"},
    {"id": 'groups/NOBS2016', "candidate": "Leni-Kiko"},
    {"id": 'groups/945591229575374', "candidate": "Leni-Kiko"},
    {"id": 'groups/2556648484480195', "candidate": "Leni-Kiko"},
    {"id": 'groups/645842846785614', "candidate": "Leni-Kiko"},
    {"id": 'groups/volunteers4leni', "candidate": "Leni-Kiko"},
    {"id": 'groups/914988072441400', "candidate": "Leni-Kiko"},


    {"id": 'iskomorenodomagoso', "candidate": "Isko-Ong"},
    {"id": 'groups/1683989658430119', "candidate": "Isko-Ong"},
    {"id": 'groups/997990110658082', "candidate": "Isko-Ong"},
    {"id": 'groups/174319694228563', "candidate": "Isko-Ong"},
    {"id": 'groups/276698607599097', "candidate": "Isko-Ong"},
    {"id": 'groups/628695250606685', "candidate": "Isko-Ong"},
    {"id": 'groups/iskonatics', "candidate": "Isko-Ong"},

    {"id": 'philstarnews', "candidate": "phil-star"},
    {"id": 'manilabulletin', "candidate": "manila-bullletin"},
    {"id": 'rappler', "candidate": "rapplerdotcom"},
    {"id": 'BanatBy', "candidate": "BanatBy"},
]

#cycle through the groups
# index_range = int(len(groups_to_scrape)/7)
# index_multiplier = datetime.datetime.today().weekday()+1
# start_range = index_range * index_multiplier
# end_range = min(start_range + index_range, len(groups_to_scrape))
# groups_to_scrape = groups_to_scrape[start_range:end_range]

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

candidate=''
while True:
    for group in groups_to_scrape:
        if candidate !=group['id'] and candidate!='':
            print('New canditate. Wait upto 1 hour.')
            wait_time = randrange(60)
            wait(60*wait_time)
        candidate=group['id']

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
            wait(time_remaining=60*15, message="The account is blocked. Waiting for 15 minutes")
            print(e)

    print('Finished looping. Scrapping will resume in 15 hours')
    wait(60*60*15)


##user scrapping
# users=database.get_all_user_with_post(limit=limit_user_scrape)
# users=users.sample(limit_user_scrape)

# known_keys=['Friend_count', 'Follower_count', 'Following_count', 'id', 'Name','Work', 'Places Lived','Life Events','Contact Info','Education', 'Basic Info','Relationship', 'Family Members', 'About', 'Friends'] 
# counter=0

# for _,user in users.iterrows():
#     try:
#         counter=0
#         profile = get_profile(str(user['user_id']), friends=10,cookies=cj)
#         #to avoid missing key error
#         json_keys = list(profile.keys())
#         for key in known_keys:
#             if key not in json_keys:
#                 profile[key]=None

#         database.insert_user(
#                 user_id=int(profile['id']), 
#                 name=profile['Name'], 
#                 friend_count=profile['Friend_count'], 
#                 follower_count=profile['Follower_count'],
#                 following_count=profile['Following_count'], 
#                 work=str(profile['Work']), 
#                 places_lived=str(profile['Places Lived']), 
#                 life_events=str(profile['Life Events']),
#                 contact_inf=str(profile['Contact Info']),
#                 education=str(profile['Education']),
#                 basic_info=str(profile['Basic Info']),
#                 relationship=str(profile['Relationship']),
#                 family_member=str(profile['Family Members']),
#                 about=str(profile['About']),
#             )

#         if profile['Friends'] is not None:
#             for friend in profile['Friends']:
#                 database.insert_connection(int(profile['id']),  int(friend['id']))

#         #avoid to many request
#         wait_time = randrange(60)
#         wait(wait_time)
#     except Exception as e:
#         print(e)
#         counter+=1
#         wait_time = randrange(120)
#         wait(time_remaining=wait_time, message="The account is blocked. Waiting for 1 minutes")
#         if counter >5: ##to count number of times the user is blocked
#             break


