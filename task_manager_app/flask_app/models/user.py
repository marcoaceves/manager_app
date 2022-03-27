# from asyncio.windows_events import NULL
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import flash

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASS_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$")
db = 'ahf_db'

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.role = data['role']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password, role) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(role)s);'
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def update_role(cls, data):
        query = "UPDATE users SET role = %(role)s WHERE users.id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def destroy_tasks(cls, data):
        query = 'DELETE FROM tasks WHERE user_id = %(id)s;'
        return connectToMySQL(db).query_db(query,data)
    @classmethod
    def destroy_likes(cls, data):
        query = 'DELETE FROM likes WHERE user_id = %(id)s;'
        return connectToMySQL(db).query_db(query,data)
    @classmethod
    def destroy_posts(cls, data):
        query =  'DELETE FROM posts WHERE user_id = %(id)s;'
        return connectToMySQL(db).query_db(query,data)
    @classmethod
    def destroy(cls, data):
        query = 'DELETE FROM users WHERE users.id = %(id)s;'
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(db).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"

        results = connectToMySQL(db).query_db(query)
        users = []

        for i in results:
            users.append( cls(i) )
        return users


# get all users and get all tasks
    @classmethod
    def get_user_and_tasks(cls,data):
        query  = "SELECT * FROM  users as user2 LEFT JOIN tasks ON user2.id = tasks.user_id WHERE user2.id =  %(user2)s;"
        results = connectToMySQL(db).query_db(query, data)
        if len(results) == 0:
            return(1)
        print(results)
        return cls(results[0])



    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])

    @staticmethod
    def validate_user( user ):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query,user)
        # test whether a field matches the pattern
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!","register")
            is_valid=False
        if not PASS_REGEX.match(user['password']):
            flash("Password must contain at least 8 characters, 1 Uppercase, 1 Lowercase, 1 Number!","register")
            is_valid=False
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters","register")
            is_valid= False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters","register")
            is_valid= False
        if len(user['role']) < 3:
            flash("")
            is_valid= False
        if user['password'] != user['confirm_password']:
            flash("Passwords don't match","register")
        return is_valid