from flask import render_template, url_for, flash, redirect, request
from flaskblog.models import User, Post
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
import json
from flask_login import login_user, current_user, logout_user, login_required

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title="register", form=form)

#login page
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Login unsuccessful. Please check your mail and password!", "danger") 
    return render_template('login.html', title="register", form=form)


#logout
@app.route("/logout")
def logout():
    logout_user()
    flash("Logout ok!", 'danger')
    return redirect(url_for('home'))


#account
@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='account')