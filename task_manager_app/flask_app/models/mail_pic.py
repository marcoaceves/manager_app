
# from winreg import QueryInfoKey
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask_app import app
from datetime import datetime
import math
from flask import flash
import smtplib

from email.message import EmailMessage

db = 'ahf_db'

class Email_Pic:
    def __init__(self, data):
        self.email = data['email']




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
        email.set_content(f"{username} has completed a Task! Please check your AHF Task Manager Dashboard!  http://54.215.222.20/")
        server.send_message(email)

