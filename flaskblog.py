from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
app = Flask(__name__)
app.config['SECRET_KEY'] = '02d239d851055e158364a8087a7fb8b4'

posts = [
    {
        'title': 'Blog Post 1',
        'author': 'Albert Einstein',
        'content': 'Photoelectric Effect ...',
        'date_posted': '05 June 1955'
    },{
        'title': 'Blog Post 2',
        'author': 'Enrico Fermi',
        'content': 'Where are the aliens?',
        'date_posted': '18 May 1959'
    }
]


#home page
@app.route("/")
@app.route("/home")
def home():
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



if __name__ == '__main__':
    app.run(debug=False)