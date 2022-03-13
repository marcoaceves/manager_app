# from winreg import QueryInfoKey
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask_app import app
from datetime import datetime
import math
from flask import flash

db = 'ahf_db'

class Task:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']


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
    def create_task(cls, data):
        query= "INSERT INTO tasks (title, user_id) VALUES (%(title)s,%(user_id)s);"
        result = connectToMySQL(db).query_db(query,data)
        return result


    @classmethod
    def get_all_tasks(cls,data):
        query = "SELECT * FROM tasks"
        results = connectToMySQL(db).query_db(query,data)
        tasks = []
        for task in results:
            tasks.append( cls(task) )
        return tasks

    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM tasks WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])


    @classmethod
    def update(cls, data):
        query = "UPDATE tasks SET title=%(title)s, WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def destroy(cls, data):
        query = 'DELETE FROM shows WHERE tasks.id = %(id)s;'
        return connectToMySQL(db).query_db(query,data)

    @staticmethod
    def validate_task( task ):
        is_valid = True

        if len(task['title']) < 3:
            flash("Show name must be at least 3 characters","task")
            is_valid= False

        return is_valid