from datetime import datetime
import json
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog.models import User, Post
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image


# home page
@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', title="home", posts=posts)

# about page
@app.route("/about")
def about():
    return render_template('about.html', title="about")


# registration page
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title="register", form=form)

# login page
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


# logout
@app.route("/logout")
def logout():
    logout_user()
    flash("Logout ok!", 'danger')
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

# account
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='account', image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='new post', form=form, legend="new post")


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title="update post", form=form, legend="update pOST")


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'danger')
    return redirect(url_for('home'))



# add sample data to POSTS
path = "/Users/erdoganb/Desktop/erdo-dev/flask_blog/flaskblog/static/blog_posts.json"
user_list = ["Albert Einstein",
             "Enrico Fermi",
             "Carl Sagan",
             "Marie Curie",
             "Chuck Yeager",
             "Jane Goodall",
             "Charles Darwin",
             "Ada Lovelace"]


@app.route('/noclip/post_sample')
def post_sample():
    db_check = Post.query.all()
    if db_check == 0:
        f = open(path, 'r')
        j = json.load(f)

        # need to arrange str format to regular date format
        def get_date(date):
            format = '%d %B %Y'
            d = datetime.strptime(date, format).date()
            return d

##BU NEDEN OLMADI BU??
        # for i in range(10):
        #     auth = get_author(i)
        #     user = user_list.index(auth)
        #     user_db = User.query.get(user)
        #     p = Post(title=get_title(i), date_posted=get_date_posted(
        #         i), content=get_content(i), author=user_db)
        #     db.session.add(p)
        #     db.session.commit()

        for i in j:
            usr = User.query.get(user_list.index(i['author'])+1)
            p = Post(title=i['title'], content=i['content'], date_posted=get_date(i['date_posted']), author=usr)
            db.session.add(p)
            db.session.commit()
    else:
        print("Database working already.")
    return "ccc"


@app.route("/noclip/user_sample")
def user_sample():
    db_check = User.query.all()
    if len(db_check) == 0:
        
        print(len(db_check))
        def get_email(user):
            sp = user.split()
            mail = sp[0] + '@' + sp[1] + ".com"
            return mail

        for i in user_list:
            u = User(username=i, email=get_email(i).lower(), password=(
                bcrypt.generate_password_hash("ccc").decode('utf-8')))
            db.session.add(u)
            db.session.commit()
    else:
        print("Database working already.")
    return "done"
