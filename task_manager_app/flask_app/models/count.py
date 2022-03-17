
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import flash

db = 'ahf_db'

class Count:
    def __init__(self, data):
        self.first_name = data['first_name']
        self.count = data['count']



# total # of tasks
    @classmethod
    def get_all_counts(cls,data):
        query = "SELECT first_name, COUNT(tasks.user_id) as count FROM  users as user2 LEFT JOIN tasks ON user2.id = tasks.user_id GROUP BY first_name"
        results = connectToMySQL(db).query_db(query,data)
        counts = []
        for count in results:
            counts.append( cls(count) )
        return counts