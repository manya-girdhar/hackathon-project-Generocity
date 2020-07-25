from flask import Flask, render_template, url_for, make_response, flash, redirect, request
from forms import RegistrationForm, LoginForm, TaskForm
import os
import time
import json
import pyrebase
from datetime import datetime

# Fixes an issue with pyrebase
def noquote(s):
    return s
pyrebase.pyrebase.quote = noquote

# Initialises Firebase
from firebase_config import firebase_config
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, static_url_path="", static_folder="../../static/", template_folder="templates/")
app.config.from_object('config')

user = False

def email_to_key(email):
    return email.replace(".", "")

def get_user_id():
    email_key = email_to_key(auth.get_account_info(auth.current_user["idToken"])["users"][0]["email"])
    all_emails = dict(db.child("emails_to_ids").get().val())
    return all_emails[email_key]


def get_user_data():
    user_id = get_user_id()
    user = dict(db.child("users").order_by_key().equal_to(user_id).get().val())[user_id]
    return user


# index route
@app.route('/')
def index():
    if auth.current_user:
        print("logged in")
    else:
        print("logged out")

    global user
    return render_template('index.html', user=user)

@app.route("/reach")
def reach():
    global user
    return render_template("reach.html", user=user)

@app.route("/login", methods=["GET", "POST"])
def login():
    # If logged in, it prevents you from going to the login page
    if auth.current_user:
       return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        try:
            auth.sign_in_with_email_and_password(form.email.data, form.password.data)
            global user
            user = get_user_data()
            flash("Login successful!", "success")
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("index"))
        except Exception as e:
            auth.current_user = None
            print("error")
            print(e)
            flash("Login Unsuccessful. Please check email and password.", "danger")

    return render_template("login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    # If logged in, it prevents you from going to the register page
    if auth.current_user:
       return redirect(url_for("index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = {
                "firstname": form.firstname.data,
                "lastname": form.lastname.data,
                "email": form.email.data,
                "location": form.location.data,
                "points": 0,
                "tasks": 0,
                "b_earnt": {
                    "welcome": True
                },
                "b_unearnt": {
                    "one": True,
                    "ten": True,
                    "fifty": True,
                    "hundred": True,
                    "climate": True,
                    "gender": True,
                    "poverty": True,
                    "education": True,
                    "hunger": True
                }
            }

            # Should return none if route doesn't exist so not none == true
            if not db.child("countries/" + form.location.data).get().val():
                c = 1
            else:
                c = db.child("countries/" + form.location.data).get().val() + 1

            key = db.generate_key()

            updates = {}
            updates["users/" + key] = user
            updates["emails_to_ids/" + email_to_key(form.email.data)] = key
            updates["countries/" + form.location.data] = c
            db.update(updates)

            # Only creates user in authentication after creating database entry
            auth.create_user_with_email_and_password(form.email.data, form.password.data)


            flash("Registered!", "success")
            return redirect(url_for("login"))
        except Exception as e:
            error = json.loads(e.args[1])['error']['message']
            if error == "EMAIL_EXISTS":
                flash("This email has already been registered.", "danger")
            print(e)
        
    return render_template("register.html", form=form)

@app.route("/account", methods=["GET", "POST"])
def account():
    if not auth.current_user:
       return redirect(url_for("index"))
    
    form = TaskForm()
    if form.validate_on_submit():
        task = {
            "title": form.title.data,
            "desc": form.desc.data,
            "timestamp": str(datetime.utcnow()),
            "p_earnt": 0, #<<<----- add function here mANYAAAA--------------------------------------------------------------
            "category": form.category.data
        }

        key = db.generate_key()
        user_id = get_user_id()
        db.child("users").child(user_id).child("tasks").update({
            key: task
        })


        flash('Your task has been added!', 'success')
        return redirect(url_for("account"))
        #^ have to do to avoid POST message...

    global user
    return render_template("user_homepage.html", user=user, form=form)

@app.route("/logout")
def logout():
    if auth.current_user:
        flash("Logout successful!", "success")
        auth.current_user = None
        global user
        user = False
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)
