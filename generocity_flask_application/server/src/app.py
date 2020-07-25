from flask import Flask, render_template, url_for, make_response
import os
import time

app = Flask(__name__, static_url_path="", static_folder="../../static/", template_folder="templates/")

# index route
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/user")
def user():
    return render_template("user_homepage.html")

if __name__ == '__main__':
    app.run(debug=True)
