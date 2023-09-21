
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '02d239d851055e158364a8087a7fb8b4'
##DATABASE
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///site.db"
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'

#password crypt
bcrypt = Bcrypt(app)

from flaskblog import routes