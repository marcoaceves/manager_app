from flask import Flask, render_template, request, json,redirect, session, flash
import requests
from flask_app import app
from flask_app.models.user import User
from flask_app.models.task import Task


DETECT_BASE_URL = 'https://google-translate1.p.rapidapi.com/language/translate/v2/detect'
TRANSLATE_BASE_URL = 'https://google-translate1.p.rapidapi.com/language/translate/v2'
HEADERS = {
    'x-rapidapi-host': "google-translate1.p.rapidapi.com",
    'x-rapidapi-key': "2c53d14e06msh2af67bbd54301e4p1625f6jsnec8d1de07b38",
    'content-type': "application/x-www-form-urlencoded"
    }



@app.route('/translate/app')
def translate_app():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }

    return render_template("translate.html",user=User.get_one(data))

@app.route('/detect', methods=['POST'])
def detect():
    # parse args
    text = request.form.get('text')

    # url encode text
    long_list_of_words = text.split(' ')
    url_encoded_text = f"source=en&target=es&q={'%20'.join(long_list_of_words)}"

    payload = url_encoded_text

    # make the request
    r = requests.post(DETECT_BASE_URL, data=payload, headers=HEADERS)

    return r.json()

@app.route('/translate', methods=['POST'])
def translate():
# parse args
    text = request.form.get('text')
    target = request.form.get('target')

    # url encode text
    long_list_of_words = text.split(' ')
    url_encoded_text = f"q={'%20'.join(long_list_of_words)}&target={target}"

    payload = url_encoded_text

    r = requests.post(TRANSLATE_BASE_URL, data=payload, headers=HEADERS)
    data=r.json()
    data2=[]
    data2.append(r.json())

    print(data2)


    return render_template('translate.html', data=data2)

