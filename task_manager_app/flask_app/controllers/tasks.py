
from dataclasses import dataclass
from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models.task import Task
from flask_app.models.user import User
from flask_app.models.post import Post
from flask_app.models.mail_auto import Email
from datetime import datetime



# html page for adding
@app.route('/task/new')
def add_new_task():
    if 'user_id' not in session:
        return redirect('/logout')
    if session['role'] == 'staff':
        return redirect("/user/dash")
    data ={
        'id': session['user_id']
    }
    return render_template('new_task.html', user=User.get_one(data), users= User.get_all())

# process adding form
@app.route('/add/task', methods=['POST'])
def add_task():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'task_name': request.form['task_name'],
        'priority': request.form['priority'],
        'due_date': request.form['due_date'],
        'complete': request.form['complete'],
        "user_id": request.form["user_id"]
    }
    data2 ={
        "id": request.form["user_id"]
    }
    user_email=Email.get_one_email(data2)
    email = user_email[0]['email']
    print(email)
    if not Task.validate_task(request.form):
        return redirect(request.referrer)
    Task.create_task(data)
    Email.send_email(email)

    return redirect ('/dashboard')



# assign station
@app.route('/assign/station', methods=['POST'])
def assign_station():
    if 'user_id' not in session:
        return redirect(request.referrer)
    data = {
        'priority': request.form['priority'],
        'due_date': request.form['due_date'],
        'complete': request.form['complete'],
        "user_id": request.form["user_id"]
    }
    if not Task.validate_station(request.form):
        return redirect(request.referrer)
    if request.form['station'] == "will_call":
        Task.assign_will_call_1(data)
        Task.assign_will_call_2(data)
        Task.assign_will_call_3(data)
        Task.assign_will_call_4(data)
        Task.assign_will_call_5(data)
        Task.assign_will_call_6(data)
        Task.assign_will_call_7(data)
    if request.form['station'] == "shipping":
        Task.assign_shipping_1(data)
        Task.assign_shipping_2(data)
        Task.assign_shipping_3(data)
        Task.assign_shipping_4(data)
        Task.assign_shipping_5(data)
        Task.assign_shipping_6(data)
    if request.form['station'] == "drop_off":
        Task.assign_drop_off_1(data)
        Task.assign_drop_off_2(data)
        Task.assign_drop_off_3(data)
        Task.assign_drop_off_4(data)
    if request.form['station'] == "station_1":
        Task.assign_station_one_1(data)
        Task.assign_station_one_2(data)
        Task.assign_station_one_3(data)
        Task.assign_station_one_4(data)
    if request.form['station'] == "station_2":
        Task.assign_station_two_1(data)
        Task.assign_station_two_2(data)

    return redirect ('/dashboard')

@app.route('/user/task/<int:user_id>')
def user_task(user_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "user2":user_id
    }
    user_data ={
        'id': session['user_id']
    }
    today=datetime.today().date()
    users= User.get_all()
    tasks = Task.get_all_user_tasks(data)

    return render_template("user_task.html",user=User.get_one(user_data), users=users, tasks=tasks, user2=User.get_user_and_tasks(data), today=today)

# process edit form
@app.route('/complete/submit', methods=['POST'])
def update_complete():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'complete': request.form['complete'],
        'id': request.form['id']
    }
    # print(data)
    Task.complete_update(data)
    return redirect(request.referrer)

@app.route('/destroy/task/', methods=['POST'])
def destroy_task():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': request.form['id']
    }
    Task.destroy(data)
    return redirect(request.referrer)