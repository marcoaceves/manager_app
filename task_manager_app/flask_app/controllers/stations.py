
from array import array
from dataclasses import dataclass
import re
from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models.task import Task
from flask_app.models.user import User
from flask_app.models.post import Post
from flask_app.models.station import Station
from datetime import datetime



# html page for adding
@app.route('/stations')
def add_new_station():
    if 'user_id' not in session:
        return redirect('/logout')
    if session['role'] == 'staff':
        return redirect("/user/dash")
    data ={
        'id': session['user_id']
    }
    return render_template('new_station.html', user=User.get_one(data), stations= Station.get_all_stations(), station_tasks=Station.get_all_stations_tasks())

# process adding form
@app.route('/add/station', methods=['POST'])
def add_station():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'name':request.form['station_name'],
        'task_name': request.form['task_name'],
    }

    Station.create_station(data)
    Task.task_added_success()
    return redirect (request.referrer)

# destroy station task

@app.route('/destroy/station/task', methods=['POST'])
def destroy_station_task():
    if 'user_id' not in session:
        return redirect('/')
    data={
            'id': request.form['id']
        }

    Station.destroy(data)
    return redirect(request.referrer)

@app.route('/destroy/station/')
def destroy_station_html():
    if 'user_id' not in session:
        return redirect('/')


    return render_template("delete_station.html", stations= Station.get_all_stations())

@app.route('/destroying/station/', methods=['POST'])
def destroy_station():
    if 'user_id' not in session:
        return redirect('/')
    data={
            'name': request.form['station_name']
        }

    Station.destroy_station(data)
    return redirect(request.referrer)
