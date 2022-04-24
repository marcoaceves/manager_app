from ast import Pass
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

    if Password.get_by_email(data)==False:
        Password.pass_email_notfound()
        return redirect(request.referrer)

    email_data=Password.get_by_email(data)
    user_id=email_data['id']
    print(user_id, "$$$$$$$$$$$")
    email=email_data['email']
    Password.send_email(email, user_id)
    Password.pass_email_success()
    return redirect(request.referrer)

@app.route('/reset_password/<token>', methods=['GET','POST'])
def reset_token(token):
    user=Password.verify_token(token)
    if user is None:
        flash('Expired Token', 'warning')
        return redirect('/forgot')
    print(user['id'],'^^^^^^^')
    return render_template("change_password.html",user=user)

@app.route('/update/password',methods=['POST'])
def update_password():
    if not Password.validate_password(request.form):
        return redirect(request.referrer)
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        'id': request.form['id'],
        'password': pw_hash,
        'confirm_password': request.form['confirm_password'],
    }
    Password.update(data)
    return redirect ('/')
