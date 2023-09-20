from flask import render_template, url_for, flash, redirect
from flaskblog.models import User, Post
from flaskblog import app
from flaskblog.forms import RegistrationForm, LoginForm
import json

# Function to parse JSON file
def parse_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Parse the JSON file at application startup
json_data = parse_json_file('flaskblog/static/blog_posts.json')


#home page
@app.route("/")
@app.route("/home")

def home():
    posts = json_data  # Access the parsed JSON data

    return render_template('home.html', title="home", posts=posts)

#about page
@app.route("/about")
def about():
    return render_template('about.html', title="about")


#registration page
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title="register", form=form)

#login page
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "a@a.a" and form.password.data=="ccc":
            flash("You've been logged in!", "success")
            return redirect(url_for('home'))
        else:
            flash("Login unsuccessful. Please check your mail and password!", "danger")
    return render_template('login.html', title="register", form=form)

