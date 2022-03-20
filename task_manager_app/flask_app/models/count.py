
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



# total # of tasks
    @classmethod
    def get_all_counts(cls,data):
        query = "SELECT first_name, user_id, COUNT(tasks.user_id) as count FROM  users LEFT JOIN tasks ON users.id = tasks.user_id GROUP BY first_name"
        results = connectToMySQL(db).query_db(query,data)
        print(results)
        counts = []
        for count in results:
            counts.append( cls(count) )
        print(counts[0].count, 'Hello World')
        return counts