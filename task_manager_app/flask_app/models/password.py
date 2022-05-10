
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import flash
import smtplib
from itsdangerous import URLSafeTimedSerializer as Serializer
from email.message import EmailMessage

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASS_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$")
db = 'ahf_db'

class Password:
    def __init__(self, data):
        self.id = data['id']
        self.email = data['email']

    @classmethod
    def update(cls,data):
        query = 'UPDATE users SET password = %(password)s WHERE id = %(id)s;'
        return connectToMySQL(db).query_db(query, data)
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT id, email FROM users WHERE email = %(email)s;"
        result = connectToMySQL(db).query_db(query,data)
        if len(result) <1  :
            return False
        return result[0]
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT id, email FROM users WHERE id = %(id)s;"
        result = connectToMySQL(db).query_db(query,data)
        # print(result[0],'^^^^^^^^^')
        return result[0]

    @staticmethod
    def pass_email_success( ):
        flash("Submit Successfully! Please Check Your Email!","email_pass")
    @staticmethod
    def pass_email_notfound( ):
        flash("Email Not Found!","email_notfound")



    @classmethod
    def get_one_email(cls,data):
        query = "SELECT email FROM users WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query,data)
        print(results)

        return results


    @staticmethod
    def send_email(receiver, user_id):
        token=Password.get_token(user_id)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        # Make sure to give app access in your Google account
        server.login('ahf.task.manager@gmail.com', 'xrhkeiruhpcazfws')
        email = EmailMessage()
        email['From'] = 'ahf.task.manager@gmail.com'
        email['To'] = receiver
        email['Subject'] = 'Password Reset Request AHF TAKS MANAGER'
        email.set_content(f"Here is your password Reset link!  http://54.215.222.20/reset_password/{token}")
        server.send_message(email)

    @classmethod
    def get_token(self, user_id):
        serial=Serializer(app.secret_key)
        return serial.dumps({'user_id':user_id})


    @staticmethod
    def verify_token(token,expiration=3600):
        serial=Serializer(app.secret_key)
        try:
            user_id=serial.loads(token,max_age=expiration)['user_id']
        except:
            flash("Your Link has expired! please resubmit Email!","invalid_token")
            return None
        data = {
        'id': user_id,
        }
        return Password.get_by_id(data)



    @staticmethod
    def validate_password( user ):
        is_valid = True
        if not PASS_REGEX.match(user['password']):
            flash("Password must contain at least 8 characters, 1 Uppercase, 1 Lowercase, 2 Numbers!","register")
            is_valid=False
        if user['password'] != user['confirm_password']:
            flash("Passwords don't match","register")
        return is_valid