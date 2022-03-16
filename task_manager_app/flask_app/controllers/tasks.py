
from dataclasses import dataclass
from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models.task import Task
from flask_app.models.user import User
from flask_app.models.post import Post


# html page for adding
@app.route('/task/new')
def add_new_task():
    if 'user_id' not in session:
        return redirect('/logout')
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
    if not Task.validate_task(request.form):
        return redirect('/task/new')
    Task.create_task(data)
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

    print(data)
    users= User.get_all()
    tasks = Task.get_all_user_tasks(data)
    return render_template("user_task.html",user=User.get_one(user_data), users=users, tasks=tasks, user2=User.get_user_and_tasks(data))

# @app.route('/details/<int:id>/<int:user_id>')
# def show_details(id, user_id):
#     if 'user_id' not in session:
#         return redirect('/logout')

#     data = {
#         "id":id,
#         "user2":user_id
#     }
#     user_data ={
#         'id': session['user_id']
#     }

#     return render_template('show_details.html', task=Task.get_one(data), user=User.get_one(user_data), user2=User.get_user_tv_show(data))


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
    return redirect ('/user/task/2')

@app.route('/destroy/task/', methods=['POST'])
def destroy_task():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': request.form['id']
    }
    Task.destroy(data)
    return redirect('/user/task/2')