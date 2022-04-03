
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

class Email:
    def __init__(self, data):
        self.email = data['email']




    @classmethod
    def get_one_email(cls,data):
        query = "SELECT email FROM users WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query,data)
        print(results)

        return results


    @staticmethod
    def send_email(receiver):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        # Make sure to give app access in your Google account
        server.login('ahf.task.manager@gmail.com', 'xrhkeiruhpcazfws')
        email = EmailMessage()
        email['From'] = 'ahf.task.manager@gmail.com'
        email['To'] = receiver
        email['Subject'] = 'AHF TAKS MANAGER'
        email.set_content("You have a New Task! Please check your AHF Task Manager Dashboard!  54.219.210.192/")
        server.send_message(email)
