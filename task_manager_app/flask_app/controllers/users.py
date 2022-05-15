from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models.user import User
from flask_app.models.task import Task
from flask_app.models.post import Post
from flask_app.models.count import Count
from flask_bcrypt import Bcrypt
import re
from datetime import datetime
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    user_check = User.get_all()
    print(user_check)
    if len(user_check) < 1 :
        return redirect ('/add/new_user/51975261726459')

    for i in user_check:
        if i == 'staff':
            return redirect ('/add/new_user/51975261726459')

    return render_template("login.html")

@app.route('/add/new_user/')
def add_user():
    if 'user_id' not in session:
        return redirect('/logout')
    if session['role'] == 'staff':
        return redirect("/user/dash")
    return render_template("add_user.html")

@app.route('/add/new_user/51975261726459')
def add_first_user():

    return render_template("add_first_user.html")

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect(request.referrer)
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'role': request.form['role'],
        'email': request.form['email'],
        'password': pw_hash,
        'confirm_password': request.form['confirm_password'],
    }
    User.save(data)
    return redirect ('/dashboard')

@app.route('/register/first/user', methods=['POST'])
def register_first_user():
    if not User.validate_user(request.form):
        return redirect(request.referrer)
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'role': request.form['role'],
        'email': request.form['email'],
        'password': pw_hash,
        'confirm_password': request.form['confirm_password'],
    }
    User.save(data)
    return redirect ('/')

@app.route('/update/role', methods=['POST'])
def update_role():
    if 'user_id' not in session:
        return redirect('/')
    data = {

        'id': request.form['id'],
        'role': request.form['role']
    }
    User.update_role(data)
    User.validate_role()
    return redirect(request.referrer)

@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password","login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password", "login")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id

    session['role'] = user_in_db.role
    if session['role'] == 'admin':
        return redirect("/dashboard")
    # never render on a post!!!
    return redirect("/user/dash")

@app.route('/user/dash')
def user_task_dash():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "user2": session['user_id']
    }
    user_data ={
        'id': session['user_id']
    }
    today=datetime.today().date()
    users= User.get_all()
    tasks = Task.get_all_user_tasks(data)
    return render_template("user_task.html",user=User.get_user_and_tasks(data), users=users, tasks=tasks, user2=User.get_one(user_data), today=today)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    if session['role'] == 'staff':
        return redirect("/user/dash")
    users= User.get_all()
    counts = Count.get_all_counts(data)


    return render_template("dashboard.html",user=User.get_one(data), users=users, counts=counts)

@app.route('/links')
def links():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    users= User.get_all()
    tasks = Task.get_all_tasks(data)
    return render_template("links.html",user=User.get_one(data), users=users, tasks=tasks)

@app.route('/manage/users')
def manage_users():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    if session['role'] == 'staff':
        return redirect("/user/dash")
    users= User.get_all()

    return render_template("manage_users.html",user=User.get_one(data), users=users,)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/destroy/user/', methods=['POST'])
def destroy_user():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': request.form['id']
    }

    User.destroy_tasks(data)
    User.destroy_likes(data)
    User.destroy_posts(data)
    User.destroy(data)
    return redirect(request.referrer)