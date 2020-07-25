from flask import Flask, render_template, url_for, make_response
from forms import RegistrationForm, LoginForm
import os
import time

app = Flask(__name__, static_url_path="", static_folder="../../static/", template_folder="templates/")
app.config.from_object('config')

# index route
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/reach")
def reach():
    return render_template("reach.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash("Registered! note: does not actually create user yet")
    return render_template("register.html", form=form)

@app.route("/user")
def user():
    return render_template("user_homepage.html")



if __name__ == '__main__':
    app.run(debug=True)
