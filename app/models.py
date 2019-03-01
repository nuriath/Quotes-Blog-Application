from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    post = db.relationship('Post',backref = 'user',lazy="dynamic")
    comment = db.relationship('Comment',backref = 'user',lazy="dynamic")
    pass_secure  = db.Column(db.String(255))
   
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)
    def __repr__(self):
        return f'User {self.username}'
        
    
class Post(db.Model):
    __tablename__ = 'post'
    author = db.Column(db.String(255))
    id = db.Column(db.Integer,primary_key = True)
    quote = db.Column(db.String(1250))
    update = db.Column(db.Integer)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    comment = db.relationship('Comment',backref = 'post',lazy="dynamic")

    def save_post(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_post(id):
        posts = Post.query.all()
        return posts

    def __repr__(self):
        return f'User {self.name}'


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    comment= db.Column(db.String(255))
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    def __repr__(self):
        return f'User {self.name}'

    def save_commet(self):
       db.session.add(self)
       db.session.commit()
