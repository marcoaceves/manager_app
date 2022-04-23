from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models.user import User
from flask_app.models.password import Password

from flask_bcrypt import Bcrypt
import re

bcrypt = Bcrypt(app)

@app.route('/forgot')
def forgot():
    user_check = User.get_all()
    print(user_check)
    if len(user_check) < 1 :
        return redirect ('/add/new_user/51975261726459')

    for i in user_check:
        if i == 'staff':
            return redirect ('/add/new_user/51975261726459')

    return render_template("forgot.html")

@app.route('/send/password/link', methods=['POST'])
def send_pass_link():

    data = {
        'email': request.form['email'],
    }
    Password.get_by_email(data)
    Password.pass_email_success()
    return redirect(request.referrer)