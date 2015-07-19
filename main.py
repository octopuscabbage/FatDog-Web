from flask import Flask, flash, redirect, render_template, request, url_for, make_response, copy_current_request_context
import requests
import json
import datetime
app = Flask(__name__)
app.secret_key = 'some_secret'

@app.route('/')
def index():
    if('fitbark-access' not in request.cookies):
        return redirect(url_for('login'))
    access_token = request.cookies['fitbark-access']

    fitbark_data = json.loads(requests.get("http://aqueous-mountain-6591.herokuapp.com/fitbark/" + str(access_token)).text)
    fitbit_data = json.loads(requests.get("http://aqueous-mountain-6591.herokuapp.com/fitbit/" ).text)

    fitbit_name = '"' + fitbit_data[0]['name'] + '"'
    fitbark_name = '"' + fitbark_data[0]['name'] + '"'

    

    fitbark_activities = map(lambda entry: entry['percent_done'],fitbark_data[0]['log'])
    fitbark_dates = map(lambda entry:  str(entry['date']),fitbark_data[0]['log'])

    fitbark_dates, fitbark_activities = fill_in_zeros(fitbark_dates,fitbark_activities)



    fitbit_activities = map(lambda entry: entry['percent_done'],fitbit_data[0]['log'])
    fitbit_dates = map(lambda entry: str(entry['date']) ,fitbit_data[0]['log'])
    
    fitbit_dates,fitbit_activities = fill_in_zeros(fitbit_dates,fitbit_activities)


    return render_template("index.html",fitbit_name=fitbit_name,fitbark_name=fitbark_name,fitbark_activities=fitbark_activities,fitbark_dates=fitbark_dates,fitbit_activities=fitbit_activities,fitbit_dates=fitbit_dates)

def fill_in_zeros(dates,activies):
    every_date_for_three_months = map(lambda days: datetime.today() - datetime.timedelta(days=days),range(1,30*3))
    out_dates = []
    out_activities = []
    
    for past_date in every_date_for_three_months:
        has_date = false
        for date in dates:
            datetime_date = datetime.datetime.strptime(string_date, "%Y-%m-%d")
            if datetime_date == date:
                has_date = true
                out_activities.append(activities[out_dates.index(date)])
        if has_date == false:
            out_activities.append(0)
    return out_dates,out_activities


                
    

def strip_to_shorter(a,b):
    if(len(a) == len(b)):
        return

    if len(a) < len (b):
        b = b[:len(a)-1]
    else:
        a = a[:len(b)-1]
    return a,b

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
