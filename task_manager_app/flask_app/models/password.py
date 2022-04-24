
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import flash
import smtplib

from email.message import EmailMessage

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASS_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$")
db = 'ahf_db'

class Password:
    def __init__(self, data):
        self.id = data['id']
        self.email = data['email']


    @classmethod
    def get_by_email(cls,data):
        query = "SELECT id, email FROM users WHERE email = %(email)s;"
        result = connectToMySQL(db).query_db(query,data)
        if len(result) <1  :
            return False
        print(result[0] ,'!!!!!!!!!!!')
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
    def send_email(usertask):
        username=usertask.first_name.capitalize()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        # Make sure to give app access in your Google account
        server.login('ahf.task.manager@gmail.com', 'xrhkeiruhpcazfws')
        email = EmailMessage()
        email['From'] = 'ahf.task.manager@gmail.com'
        email['To'] = 'mr.aceves@gmail.com'
        email['Subject'] = 'Task Completed! AHF TAKS MANAGER'
        email.set_content(f"{username} has completed a Task! Please check your AHF Task Manager Dashboard!  http://54.193.73.88/")
        server.send_message(email)
