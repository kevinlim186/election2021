import src.config as config
import pymysql
import pandas as pd
from random import randint
from io import StringIO


class Database():
    def __init__(self):
        self.conn = None
        self.cHandler = None    
        self.comment_ids = None
        self.post_ids = None
        self.intializeConnection()
        self.get_comment_ids()
        self.get_post_ids()

    def intializeConnection(self):
        self.conn = pymysql.connect(host='127.0.0.1', user=config.config['db_user'],
                        passwd=config.config['db_pass'], db=config.config['db_schema'],
                        port=config.config['localPort'],autocommit=True)
        self.cHandler = self.conn.cursor()

    def insert_comment(self, post_id, comment_id, _text, time_stamp, user_id, username):

        if comment_id not in self.comment_ids['comment_id'].values:
            sql = '''
            insert into comments (post_id, comment_id, _text, time_stamp, user_id, username)
            values (%s,%s,%s,%s,%s,%s)
            '''

            try:
                self.cHandler.execute(sql, (post_id, comment_id, _text, time_stamp, user_id, username))

                self.comment_ids= self.comment_ids.append({'comment_id':comment_id}, ignore_index=True)
            except Exception as e: 
                pass
        else:
            print('Comment is already in the database')

    
    def insert_post(self, post_id, _text, time_stamp, likes, comments, shares, user_id, username, group_id, group_candidate):

        if post_id not in self.post_ids['post_id'].values:
            try:
                sql = '''
                insert into posts (post_id, _text, time_stamp, likes, comments, shares, user_id, username,group_id, group_candidate)
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                '''
        
                self.cHandler.execute(sql, (post_id, _text, time_stamp, likes, comments, shares, user_id, username,group_id, group_candidate))

                self.post_ids= self.post_ids.append({'post_id':post_id}, ignore_index=True)
            except Exception as e: 
                pass
        
        else:
            sql = '''
            update posts
            set likes = %s,
            comments = %s,
            shares = %s
            where post_id = %s
            '''
    
            self.cHandler.execute(sql, ( likes, comments, shares, post_id))
            print('Updating Post {}'.format(post_id))

    def get_comment_ids(self):
        sql = 'select comment_id from comments'
        
        self.comment_ids = pd.read_sql_query(sql=sql, con=self.conn)
    
    def get_post_ids(self):
        sql = 'select post_id from posts'
        
        self.post_ids = pd.read_sql_query(sql=sql, con=self.conn)

    def get_texts(self):
        sql = '''
            select comments._text, group_candidate
            from comments
            inner join posts on comments.post_id = posts.post_id
            group by comments._text, group_candidate
            union 
            select  _text, group_candidate
            from posts
            group by  _text, group_candidate
        '''

        return pd.read_sql_query(sql=sql, con=self.conn)