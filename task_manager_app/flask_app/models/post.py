# from winreg import QueryInfoKey
from types import ClassMethodDescriptorType
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask_app import app
from datetime import datetime
import math
from flask import flash

db = 'ahf_db'

class Post:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.total_likes = data['total_likes']

    # def time_span(self):
    #     now = datetime.now()
    #     delta = now - self.created_at
    #     print(delta.days)
    #     print(delta.total_seconds())
    #     if delta.days > 0:
    #         return f"{delta.days} day(s) ago"
    #     elif (math.floor(delta.total_seconds() / 60)) >= 60:
    #         return f"{math.floor(math.floor(delta.total_seconds() / 60)/60)} hour(s) ago"
    #     elif delta.total_seconds() >= 60:
    #         return f"{math.floor(delta.total_seconds() / 60)} minute(s) ago"
    #     else:
    #         return f"{math.floor(delta.total_seconds())} second(s) ago"

    @classmethod
    def create_post(cls, data):
        query= "INSERT INTO posts (content, user_id) VALUES (%(content)s,%(user_id)s);"
        result = connectToMySQL(db).query_db(query,data)
        return result

# total # of tasks
    @classmethod
    def get_all_posts(cls,data):
        query = """SELECT first_name as first_name, ANY_VALUE(user2.id) as user_id, ANY_VALUE(posts.id) as id, ANY_VALUE(posts.created_at) as created_at, ANY_VALUE(posts.updated_at) as updated_at, count(post_id) as total_likes,  ANY_VALUE(content) as content
        FROM  users as user2 JOIN posts ON user2.id = posts.user_id LEFT JOIN likes ON posts.id = likes.post_id  GROUP BY created_at ORDER by posts.id DESC"""
        results = connectToMySQL(db).query_db(query,data)
        # print(results)
        posts = []
        if results==False:
            return None
        for post in results:
            posts.append( cls(post) )
        # print('POST',posts)
        return posts

    @classmethod
    def get_one_post(cls,data):
        query  = "SELECT * FROM posts WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE posts SET content=%(content)s, WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def destroy(cls, data):
        query = 'DELETE FROM posts WHERE posts.id = %(id)s;'
        return connectToMySQL(db).query_db(query,data)

    @staticmethod
    def validate_post( task ):
        is_valid = True
        if len(task['title']) < 3:
            flash("Post must be at least 3 characters","task")
            is_valid= False
        return is_valid

    @classmethod
    def like(cls, data):
        query= "INSERT INTO likes (user_id, post_id) VALUES (%(user_id)s,%(post_id)s);"
        result = connectToMySQL(db).query_db(query,data)
        return result

    @classmethod
    def destroy_like(cls, data):
        query = 'DELETE FROM likes WHERE post_id = %(post_id)s AND user_id = %(user_id)s;'
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_likes_by_id(cls,data):
        query = "SELECT *  FROM likes WHERE post_id = %(post_id)s AND user_id = %(user_id)s;"
        result = connectToMySQL(db).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])