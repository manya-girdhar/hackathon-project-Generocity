from flask import Flask, render_template, url_for, make_response, flash, redirect
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

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("Logged in! note: not actually logged in", "success")
        return redirect(url_for("index"))
    return render_template("login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash("Registered! note: does not actually create user yet", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/user")
def user():
    return render_template("user_homepage.html")



if __name__ == '__main__':
    app.run(debug=True)
