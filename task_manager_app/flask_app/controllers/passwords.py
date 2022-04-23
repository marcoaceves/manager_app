from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models.user import User

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

@app.route('/send/password/link')
def send_pass_link():
    User.get_one()