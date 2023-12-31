from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskblog import app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#DATABASE MODELS
class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False) #passwords will be hashed!
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    def get_reset_token(self, expires_seconds=600):
        s = Serializer(app.config['SECRET_KEY'], expires_seconds)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

class Post(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)##remove nullable! due to an error
    ##datetime.utcnow is a function!
    ##datetime.utcnow() return of a function!
    content = db.Column(db.Text, nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))##remove nullable! due to an error
#error was-> TypeError: Additional arguments should be named <dialectname>_<argument>, got 'nullabe'

    def __repr__(self):
        return f"Post('{self.title}','{self.content}','{self.author}', '{self.date_posted}')"