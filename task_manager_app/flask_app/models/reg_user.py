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

class Register_User:
    def __init__(self, data):
        self.id = data['id']
        self.pharmacy_name = data['pharmacy_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO reg_users (pharmacy_name, email, password) VALUES (%(pharmacy_name)s, %(email)s, %(password)s);'
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM reg_users WHERE email = %(email)s;"
        result = connectToMySQL(db).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_one(cls,data):
        query  = "SELECT id, pharmacy_name, email, created_at, updated_at FROM reg_users WHERE id = %(reg_user_id)s;"
        
        results = connectToMySQL(db).query_db(query, data)
        results[0]["password"] = ""
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
            flash("Password must contain at least 8 characters, 1 Uppercase, 1 Lowercase, 2 Numbers!","register")
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

    @staticmethod
    def validate_role( ):
        flash("Role Updated Successfully!","updated")


