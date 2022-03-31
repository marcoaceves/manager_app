
# from winreg import QueryInfoKey
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask_app import app
from datetime import datetime
import math
from flask import flash

db = 'ahf_db'

class Like:
    def __init__(self, data):
        self.user_id = data['user_id']
        self.post_id = data['post_id']


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
    def create_like(cls, data):
        query= "INSERT INTO likes (user_id, post_id) VALUES (%(user_id)s,%(post_id)s);"
        result = connectToMySQL(db).query_db(query,data)
        return result

    @classmethod
    def get_all_likes(cls,data):
        query = "SELECT * FROM likes"
        results = connectToMySQL(db).query_db(query,data)
        tasks = []
        for task in results:
            tasks.append( cls(task) )
        return tasks

    @classmethod
    def get_one_like(cls,data):
        query  = "SELECT * FROM likes WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])


    @classmethod
    def destroy(cls, data):
        query = 'DELETE FROM likes WHERE comments.id = %(id)s;'
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_likes_by_id(cls,data):
        query = "SELECT *  FROM likes WHERE post_id = %(post_id)s AND user_id = %(user_id)s;"
        result = connectToMySQL(db).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])