
from array import array
from dataclasses import dataclass
import re
from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models.task import Task
from flask_app.models.user import User
from flask_app.models.station import Station
from flask_app.models.mail_auto import Email
from flask_app.models.mail_pic import Email_Pic
from datetime import datetime
import calendar




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
    return render_template('new_task.html', user=User.get_one(data), users= User.get_all(),stations= Station.get_all_stations() )

# process adding form
@app.route('/add/task', methods=['POST'])
def add_task():
    if 'user_id' not in session:
        return redirect('/')
    if not Task.validate_task(request.form):
        return redirect(request.referrer)
    dates= request.form['due_date'].split(',')
    for x in range(len(dates)):
        data = {
            'task_name': request.form['task_name'],
            'priority': request.form['priority'],
            'due_date': dates[x],
            'complete': request.form['complete'],
            "user_id": request.form["user_id"]
        }
        if data['task_name'] != 'NULL':
            Task.create_task(data)
    data2 ={
        "id": request.form["user_id"]
    }
    user_email=Email.get_one_email(data2)
    email = user_email[0]['email']

    Email.send_email(email)
    Task.task_added_success()
    return redirect (request.referrer)

# html page for editing task
@app.route('/edit/<int:task_id>')
def edit_task(task_id):
    if 'user_id' not in session:
        return redirect('/logout')
    if session['role'] == 'staff':
        return redirect("/user/dash")
    data ={
        'id': task_id
    }
    user_id = Task.get_one(data).user_id
    user_data={
        'id': user_id
    }


    return render_template('edit_task.html',  task=Task.get_one(data), user=User.get_one(user_data)  )

# route for processing edit
@app.route('/edit/task', methods=['POST'])
def edit_task_process():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'task_name': request.form['task_name'],
        'due_date': request.form['due_date'],
        'complete': request.form['complete'],
        'id' : request.form['task_id']
    }


    Task.edit_task(data)
    Task.task_added_success()
    return redirect (request.referrer)

# prep task calendar assing form
@app.route('/prep/task', methods=['POST'])
def add_prep():
    if 'user_id' not in session:
        return redirect('/')
    prep_arr=request.form
    new_arr = []

    for i in range(32):
        if "task_name"+str(i+1) in prep_arr:
            new_arr.append("Prep LA"+ str(i+1).zfill(2))

    if not Task.validate_task_date(request.form):
            return redirect(request.referrer)
    for i in range(len(new_arr)):
        data = {
            'task_name': new_arr[i],
            'priority': request.form['priority'],
            'due_date': request.form['due_date'],
            'complete': request.form['complete'],
            "user_id": request.form["user_id"]
        }

        Task.create_task(data)
    Task.task_added_success()

    return redirect (request.referrer)
    # text task calendar form
@app.route('/text/task', methods=['POST'])
def add_text():
    if 'user_id' not in session:
        return redirect('/')
    prep_arr=request.form
    new_arr = []
    for i in range(32):
        if "task_name"+str(i+1) in prep_arr:
            new_arr.append("Text LA"+ str(i+1).zfill(2))
    if not Task.validate_task_text(request.form):
            return redirect(request.referrer)
    for i in range(len(new_arr)):
        data = {
            'task_name': new_arr[i],
            'priority': request.form['priority'],
            'due_date': request.form['due_date'],
            'complete': request.form['complete'],
            "user_id": request.form["user_id"]
        }

        Task.create_task(data)
    Task.task_added_success()

    return redirect (request.referrer)
    # refill task calendar form
@app.route('/refill/task', methods=['POST'])
def add_refill():
    if 'user_id' not in session:
        return redirect('/')
    prep_arr=request.form
    new_arr = []
    for i in range(32):
        if "task_name"+str(i+1) in prep_arr:
            new_arr.append("Refill Requests LA"+ str(i+1).zfill(2))
    if not Task.validate_task_refill(request.form):
            return redirect(request.referrer)
    for i in range(len(new_arr)):
        data = {
            'task_name': new_arr[i],
            'priority': request.form['priority'],
            'due_date': request.form['due_date'],
            'complete': request.form['complete'],
            "user_id": request.form["user_id"]
        }

        Task.create_task(data)
    Task.task_added_success()

    return redirect (request.referrer)



# assign station
@app.route('/assign/station', methods=['POST'])
def assign_station():
    if 'user_id' not in session:
        return redirect('/')
    data = {
            'name': request.form['station_name']
            }
    station=Station.get_one_stations_tasks(data)

    if not Task.validate_station(request.form):
        return redirect(request.referrer)

    word = 'Tuesday'
    tuesday = ''

    dates=request.form['due_date'].split(',')
    for x in range(len(dates)):
        Myday= datetime.strptime(dates[x], '%Y-%m-%d').date()
        for i in range(len(station)):

            data = {
                'task_name': station[i].task_name,
                'priority': request.form['priority'],
                'due_date': dates[x],
                'complete': request.form['complete'],
                "user_id": request.form["user_id"]
            }
            if word in station[i].task_name:
                tuesday = "Tuesday"
                if calendar.day_name[Myday.weekday()] == tuesday:
                    Task.create_task(data)
                else:print('hello')
            else:
                if data['task_name'] != 'NULL':
                    Task.create_task(data)
            tuesday = ''
    Task.task_added_success()
    return redirect (request.referrer)

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

    Task.complete_update(data)

    return redirect(request.referrer)
# add comment to task form
@app.route('/task/comment', methods=['POST'])
def comment_task():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'comment': request.form['comment'],
        'id': request.form['id']
    }
    # print(data)
    Task.update_comment(data)
    return redirect(request.referrer)

@app.route('/update/task/', methods=['POST'])
def update_tasks():
    if 'user_id' not in session:
        return redirect('/')
    if request.method == "POST":
        checked_list=request.form.getlist('checked1')
    for i in range(len(checked_list)):
            data = {
            'id': checked_list[i]}
            Task.destroy(data)
    user2data = {
        "user2": request.form['user2_id']
    }
    completed=request.form.getlist('complete')
    status=request.form.getlist('status')
    print(completed, "TTTTTTTTTTT")
    print(status, "TTTTTTTTTTT")
    user2data=User.get_user_and_tasks(user2data)
    for i in range(len(completed)):
            data = {
            'id': completed[i]}
            data2=Task.get_one(data)
            if hasattr(data2, 'complete'):
                if data2.complete != None:
                    if (status[i] == '1'):
                        data = {
                    'id': completed[i],
                    'complete': '1',
                    'status':status[i]}
                        Task.complete_update(data)
                    if (status[i] != '1'):
                        data = {
                    'id': completed[i],
                    'complete': '0',
                    "status":status[i]}
                        Task.complete_update(data)
    if len(completed) > 0:
        data = {
                'id': completed[i]}
        data2=Task.get_one(data)
        if hasattr(data2, 'complete'):
            if data2.complete != None:
                Email_Pic.send_email(user2data)
                Task.task_updated_success()


    comments=request.form.getlist('comment')
    for i in range(len(comments)-1):
            data = {
            'comment': comments[i+1],
            'id': comments[i]}
            if comments[i+1]=="":
                data2=Task.get_one(data)
                data = {
            'comment': data2.comment,
            'id': comments[i]}
            i+=1
            Task.update_comment(data)


    return redirect(request.referrer)