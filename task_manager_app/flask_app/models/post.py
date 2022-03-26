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
        self.likes = 0  #increment this number



    def time_span(self):
        now = datetime.now()
        delta = now - self.created_at
        print(delta.days)
        print(delta.total_seconds())
        if delta.days > 0:
            return f"{delta.days} day(s) ago"
        elif (math.floor(delta.total_seconds() / 60)) >= 60:
            return f"{math.floor(math.floor(delta.total_seconds() / 60)/60)} hour(s) ago"
        elif delta.total_seconds() >= 60:
            return f"{math.floor(delta.total_seconds() / 60)} minute(s) ago"
        else:
            return f"{math.floor(delta.total_seconds())} second(s) ago"

    @classmethod
    def create_post(cls, data):
        query= "INSERT INTO posts (content, user_id) VALUES (%(content)s,%(user_id)s);"
        result = connectToMySQL(db).query_db(query,data)
        return result


# total # of tasks
    @classmethod
    def get_all_posts(cls,data):
        query = "SELECT first_name, user2.id as user_id, posts.id as id, posts.created_at, posts.updated_at,  content FROM  users as user2 LEFT JOIN posts ON user2.id = posts.user_id GROUP BY created_at"
        "SELECT first_name, user2.id as user_id, sum(complete) as complete, task_name, COUNT(tasks.user_id) as count FROM  users as user2 LEFT JOIN tasks ON user2.id = tasks.user_id GROUP BY first_name"
        results = connectToMySQL(db).query_db(query,data)
        print(results)
        posts = []
        for post in results:
            posts.append( cls(post) )
        print('POST',posts)
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


# Likes class method
    @classmethod
    def get_all_likes(cls):
        query = """
        SELECT * FROM posts LEFT JOIN likes ON posts.id = likes.post_id;
        """
        results = connectToMySQL(db).query_db(query)
        posts = []
        for post in results:
            # print(post)
            current_post = {
                "id" : post["id"],
                "content" : post["content"],
                "created_at" : post["updated_at"],
                "created_at" : post["updated_at"],
            }

            # checking if we have already added this post to the post list/array
            if len(posts) == 0:
                posts.append(cls(current_post)) #if an array is empty we add the post
            else:
                last_post = posts[len(posts) - 1]

                if last_post.id != current_post ["id"]:
                    posts.append(cls(current_post))

            last_post = posts[len(posts) - 1]

            last_post.likes += 1
        return posts

    @classmethod
    def like(cls, data):
        query= "INSERT INTO likes (user_id, post_id) VALUES (%(user_id)s,%(post_id)s);"
        result = connectToMySQL(db).query_db(query,data)
        return result