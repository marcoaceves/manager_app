
from array import array
from dataclasses import dataclass
import re
from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models.user import User
from flask_app.models.station import Station
from flask_app.models.signoffsheet import Register
from datetime import datetime
import datetime as dt


# html page for adding
@app.route('/signoffsheet')
def signoff_sheet_display():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }

    register =Register.get_signoff_sheet()
    for reg in register:
        if reg.name==None:
            reg.name=""
        if reg.tech_initial==None:
            reg.tech_initial=""
        if reg.rph_initial==None:
            reg.rph_initial=""
    return render_template('register_signoff.html', user=User.get_one(data), register=register)

# process adding form
# month +=1 checks currnet then add if 12 then mnth == 1
@app.route('/delete/create/new')
def delete_create_new_signoff():
    if 'user_id' not in session:
        return redirect('/')
    Register.destroy()
    for day in  range(1,32):
        month = datetime.today().month
        year = datetime.today().year
        print(month, year, '*****')
        try:
            date = dt.date(year,month,day)
        except:
            return redirect ("/signoffsheet")
        data={"date":date}
        print(data, date)
        Register.create_signoff_sheet(data)

    return redirect ("/signoffsheet")

@app.route('/update/signoff_sheet', methods=['POST'])
def update_signoff():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'name': request.form['name'],
        'tech_initial': request.form['tech_initial'],
        'rph_initial': request.form['rph_initial'],
        'id': request.form['id']
    }

    Register.signoff_update(data)
    return redirect(request.referrer)