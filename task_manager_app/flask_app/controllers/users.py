
from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models.user import User
from flask_app.models.task import Task
from flask_bcrypt import Bcrypt
import re
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/add/new_user/')
def add_user():
    return render_template("add_user.html")

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash,
        'confirm_password': request.form['confirm_password'],
    }
    User.save(data)

    login_data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(login_data)
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


    return redirect ('/dashboard')

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
    # never render on a post!!!
    return redirect("/dashboard")


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    users= User.get_all()
    tasks = Task.get_all_tasks(data)
    return render_template("dashboard.html",user=User.get_one(data), users=users, tasks=tasks)

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


@app.route('/user/task')
def user_task():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    users= User.get_all()
    tasks = Task.get_all_tasks(data)
    return render_template("user_task.html",user=User.get_one(data), users=users, tasks=tasks)

@app.route('/manage/users')
def manage_users():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    users= User.get_all()

    return render_template("manage_users.html",user=User.get_one(data), users=users,)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')