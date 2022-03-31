# from winreg import QueryInfoKey
"""
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask_app import app
from datetime import datetime
import math
from flask import flash

db = 'ahf_db'

class Comment:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.post_id = data['post_id']

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
    def create_comment(cls, data):
        query= "INSERT INTO comments (content, user_id, post_id) VALUES (%(title)s,%(user_id)s,%(post_id)s);"
        result = connectToMySQL(db).query_db(query,data)
        return result

    @classmethod
    def get_all_comments(cls,data):
        query = "SELECT * FROM comments"
        results = connectToMySQL(db).query_db(query,data)
        tasks = []
        for task in results:
            tasks.append( cls(task) )
        return tasks

    @classmethod
    def get_one_comment(cls,data):
        query  = "SELECT * FROM comments WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE comments SET title=%(content)s, WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def destroy(cls, data):
        query = 'DELETE FROM comments WHERE comments.id = %(id)s;'
        return connectToMySQL(db).query_db(query,data)

    @staticmethod
    def validate_comment( comment ):
        is_valid = True

        if len(comment['content']) < 3:
            flash("Comment must be at least 3 characters","task")
            is_valid= False

        return is_valid
"""