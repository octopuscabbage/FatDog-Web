from flask import Flask, flash, redirect, render_template, request, url_for, make_response, copy_current_request_context
import requests
import json
app = Flask(__name__)
app.secret_key = 'some_secret'

@app.route('/')
def index():
    if('fitbark-access' in request.cookies):
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':

        json_data = json.dumps({"login":{"username": str(request.form['username']), "password": str(request.form['password'])}})
        header = {"Accepts":"application/json","Content-Type":"application/json"}
        data = json.loads(requests.post("http://app.fitbark.com/api/login",headers=header,data=json_data).text)
        if 'error' in data:
            error = 'Invalid credentials'
        else:
            flash('You were successfully logged in')
            resp = make_response(render_template("index.html"))
            resp.set_cookie('fitbark-access',data['session']['access_token']) 
            return resp
    return render_template('fitbark_login.html', error=error)
app.debug = True
