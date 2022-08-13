from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models.reg_user import Register_User
from flask_app.models.multi_reg import Multi_Register
from flask_app.models.count import Count
from flask_bcrypt import Bcrypt
import re
from datetime import datetime
import datetime as dt
bcrypt = Bcrypt(app)

# this controller is used for users who are only allowed to access register signoff sheet

@app.route('/register/login')
def multi_register_login():

    return render_template("multi_register_login.html")

@app.route('/login/multiregister', methods=['POST'])
def loginquery_multireg():
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = Register_User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password","login")
        return redirect("/register/login")
    if not user_in_db.password== request.form['password']:
        # if we get False after checking the password
        flash("Invalid Email/Password", "login")
        return redirect('/register/login')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id

    # never render on a post!!!
    return redirect("/signoffsheet/multi")

@app.route('/signoffsheet/multi')
def multi_signoff_sheet_display():
    if 'user_id' not in session:
        return redirect('/logout/multiregister')
    data ={
        'reg_user_id': session['user_id']
    }

    register =Multi_Register.get_signoff_sheet(data)
    for reg in register:
        if reg.name==None:
            reg.name=""
        if reg.rph_initial==None:
            reg.rph_initial=""
    return render_template('multi_register_signoff_sheet.html', user=Register_User.get_one(data), register=register)


    # process adding form
# month +=1 checks currnet then add if 12 then mnth == 1
@app.route('/delete/create/new/multi')
def delete_create_new_signoff_multi():
    if 'user_id' not in session:
        return redirect('/')
    data ={
        'reg_user_id': session['user_id']
    }
    Multi_Register.destroy(data)
    for day in  range(1,32):
        month = datetime.today().month
        year = datetime.today().year
        print(month, year, '*****')
        try:
            date = dt.date(year,month,day)
        except:
            return redirect ("/signoffsheet")
        data={"date" : date ,
        'reg_user_id': session['user_id']
        }
        print(data, date)
        Multi_Register.create_signoff_sheet(data)


    return redirect (request.referrer)

@app.route('/update/signoff_sheet/multi', methods=['POST'])
def update_signoff_multi():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'name': request.form['name'],
        'rph_initial': request.form['rph_initial'],
        'id': request.form['id']
    }

    Multi_Register.signoff_update(data)
    flash(" Register Sheet Successfully Upadated!", "update")
    return redirect(request.referrer)



@app.route('/logout/multiregister')
def regsheet_logout():
    session.clear()
    return redirect('/register/login')
