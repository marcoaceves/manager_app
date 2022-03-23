
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import flash

db = 'ahf_db'

class Count:
    def __init__(self, data):
        self.user_id = data['user_id']
        self.first_name = data['first_name']
        self.count = data['count']
        self.complete = data['complete']



# total # of tasks
    @classmethod
    def get_all_counts(cls,data):
        query = "SELECT first_name, user2.id as user_id, sum(complete) as complete, task_name, COUNT(tasks.user_id) as count FROM  users as user2 LEFT JOIN tasks ON user2.id = tasks.user_id GROUP BY first_name"
        results = connectToMySQL(db).query_db(query,data)
        print(results)
        counts = []
        for count in results:
            counts.append( cls(count) )
        print("COUNTS",counts)
        return counts



