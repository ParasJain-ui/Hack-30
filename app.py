import json
import os
import sqlite3
from flask import Flask, redirect, request, url_for,render_template
from flask_login import (LoginManager,current_user,login_required,login_user,logout_user,)
from oauthlib.oauth2 import WebApplicationClient
import requests
from db import init_db_command
from user import User
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from scoreCalculator import score_calculation, allot_date
# from FormData import Application
# GOOGLE_CLIENT_ID = config{"GOOGLE_CLIENT_ID"}
# GOOGLE_CLIENT_SECRET = config{"GOOGLE_CLIENT_SECRET"}



#mentioned in report
GOOGLE_CLIENT_ID=""
GOOGLE_CLIENT_SECRET=""
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

app = Flask(__name__)

#creating database
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
app.config['SQLALCHEMY_BINDS'] = {"slots": 'sqlite:///slots.db'}
database=SQLAlchemy(app)

class Application(database.Model):
    id=database.Column(database.Integer,primary_key=True)
    fname=database.Column(database.String(50), nullable=False)
    lname=database.Column(database.String(50), nullable=False)
    r_n=database.Column(database.String(200), nullable=False)
    apply_date = database.Column(database.String(200), nullable=True)
    preference_1 = database.Column(database.String(200), nullable=False)
    preference_2 = database.Column(database.String(200), nullable=False)
    phone_number=database.Column(database.String(12),nullable=False)
    gender=database.Column(database.String(12), nullable=False)
    age=database.Column(database.String(12),nullable=False)
    city=database.Column(database.String(24), nullable=False)
    state=database.Column(database.String(24), nullable=False)
    programme=database.Column(database.String(24), nullable=False)
    year=database.Column(database.String(12), nullable=False)
    branch=database.Column(database.String(12), nullable=False)
    travel_mode=database.Column(database.String(12), nullable=False)
    cllg_equip=database.Column(database.String(24), nullable=False)
    symptoms=database.Column(database.String(24), nullable=False)
    rtd=database.Column(database.String(24), nullable=False)
    description=database.Column(database.String(300), nullable=False)
    alloted_date=database.Column(database.String(12), nullable=True)
    score = database.Column(database.Integer, nullable=False, default=0)
    isProcessed = database.Column(database.Boolean, default=False)
    
    def __repr__(self):
        return '<Application %r>' % self.id

class Slots(database.Model):
    __bind_key__ = 'slots'
    id=database.Column(database.Integer,primary_key=True)
    date = database.Column(database.String(200), nullable=False)
    num_slots = database.Column(database.Integer, default=10, nullable=False)

    def __repr__(self):
        return '<Slots %r>' % self.id

app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
login_manager = LoginManager()
login_manager.init_app(app)
try:
    init_db_command()
except sqlite3.OperationalError:
    pass
client = WebApplicationClient(GOOGLE_CLIENT_ID)
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
@app.route('/',methods=['Post','Get'])
def index():
    if current_user.is_authenticated:
        # return (
        #     "<p>Hello, {}! You're logged in! Email: {}</p>"
        #     "<div><p>Google Profile Picture:</p>"
        #     '<img src="{}" alt="Google profile pic"></img></div>'
        #     '<a class="button" href="/logout">Logout</a>'.format(
        #         current_user.name, current_user.email, current_user.profile_pic
        #     )
        # )
        return redirect('/application')
    else:
        return '<a class="button" href="/login">Login</a><br><a class="button" href="/admin">or are you admin?</a><br><a href="/database">Database</a>'
def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()
@app.route("/login")
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],

    )
    return redirect(request_uri)
xyz=False
@app.route('/') 
@app.route('/admin', methods =['GET', 'POST']) 
def admin(): 
    msg = '' 
    if request.method == 'POST': 
        username = request.form['username'] 
        password = request.form['password'] 
        if(username=="admin" and password=="admin" ):
            # task = Application.query.all()
            global xyz
            xyz=True
            return redirect('/applications') 
        else: 
            msg = 'Incorrect username / password !'
    return render_template('admin.html', msg = msg)
        
@app.route("/login/callback")
def callback():
    code = request.args.get("code")
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )
    client.parse_request_body_response(json.dumps(token_response.json()))
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400
    user = User(
    id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)
    login_user(user)
    return redirect(url_for("index"))
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/application", methods=['GET', 'POST'])
def application():
    # print(type(current_user.email))
    # print(len(list(Application.query.filter_by(r_n=current_user.email))))
    try:
        if len(list(Application.query.filter_by(r_n=current_user.email))):
            temp_user = Application.query.filter_by(r_n=current_user.email).first()
            if temp_user.alloted_date:
                return f"<h1>Congrats. Your alloted date is {temp_user.alloted_date}</h1><br><a class='button' href='/logout'>Logout</a>"
            #should return date
            else:
                return "<h1>Your application has already been submitted. Wait for sometime to get the alloted date.</h1><br><a class='button' href='/logout'>Logout</a>"
        else:
            if request.method == 'POST':
                req = request.form

                score = score_calculation(req)

                task=Application(fname=req['fname'],
                                lname=req['lname'],
                                r_n=req['roll_number'],
                                phone_number=req["phone_number"],
                                gender=req["gender"],
                                age=req["age"],
                                apply_date = date.today(),
                                city=req["city"],
                                state=req["state"],
                                programme=req["programme"],
                                year=req["year"],
                                branch=req["branch"],
                                travel_mode=req["travel_mode"],
                                cllg_equip=req["cllg_equip"],
                                symptoms=req["symptoms"],
                                rtd=req["recent_travel_date"],
                                description=req["description"],
                                preference_1=req["preference_1"],
                                preference_2=req["preference_2"],
                                score = score)
                try:
                    database.session.add(task)
                    database.session.commit()
                    return '<h1>successful</h1><br><a class="button" href="/logout">Logout</a>'
                except:
                    return '<h1>error</h1><br><a class="button" href="/logout">Logout</a>'
            else:
                return render_template("form.html",r_n=current_user.email)
            return render_template("form.html")
    except:
        return '<h1>Please Login First or fill the details correctly</h1>'
@app.route('/applications',methods=['GET','POST'])
def applications():
    # if request.method == "POST":
    #     date = request.form['date']
    #     task = Slots(date=date)

    #     database.session.add(task)
    #     database.session.commit()
    #     return redirect(url_for("applications"))
    if(xyz):
        if request.method=="POST":
            a=Application.query.filter_by(id=request.form['id']).first()
            if(not a.isProcessed):
                a.score += int(request.form['score'])
                a.isProcessed = True
                database.session.commit()
            return redirect(url_for("applications"))
        else:
            task = Application.query.filter_by(isProcessed=False)
            if len(list(task)) == 0:
                null_dates = list(Application.query.filter_by(alloted_date=None))
                available_slots = list(Slots.query.all())

                if(len(null_dates)):
                    ids, dates = allot_date(null_dates, available_slots)
                    print(len(dates), len(ids))

                    for i in range(len(null_dates)):
                        print(i)
                        row = Application.query.filter_by(id = ids[i]).first()
                        row.alloted_date = dates[i]
                        d = Slots.query.filter_by(date = dates[i]).first()
                        d.num_slots -= 1
                        database.session.commit()


                #     null_dates[i].alloted_date = dates[i]
                #     database.session.commit()

                
        

            return render_template("applications.html",task=task, available_slots=Slots.query.all())
    else:
        return '<h1>Please Login</h1>'

@app.route('/database', methods=['GET', 'POST'])
def databaseabc():
    return render_template("database.html",task=Application.query.all(), available_slots=Slots.query.all())


if __name__ == "__main__":
    app.run(ssl_context="adhoc", debug=True)
