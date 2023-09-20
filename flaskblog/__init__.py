
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '02d239d851055e158364a8087a7fb8b4'
##DATABASE
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///site.db"
db = SQLAlchemy(app)

from flaskblog import routes