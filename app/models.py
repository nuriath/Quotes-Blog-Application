from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Quote:

    # all_quotes = []

    def __init__(self,id,author,quote):
        self.id =id
        self.author = author
        self.quote = quote
     
        
    # def save_quotes(self):
    #    Quote.all_quotes.append(self)


    # @classmethod
    # def clear_quotes(cls):
    #    Post.all_quotes.clear()

    # @classmethod
    # def get_quotes(cls,id):

    #     response = []

    #     for Quote in cls.all_quotes:
    #         if Quote.user_id == id:
    #             response.append(quote)

    #     return response

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
    __tablename__ = 'posts'

    id = db.Column(db.Integer,primary_key = True)
    post = db.Column(db.String(1250))
    update = db.Column(db.Integer)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    comment = db.relationship('Comment',backref = 'posts',lazy="dynamic")

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
    post_id = db.Column(db.Integer,db.ForeignKey('posts.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(id):
        comments = Comment.query.all()
        return comments

    def delete(self):
       db.session.delete(self)
       db.session.commit()


class Subscribe(db.Model):
    __tablename__= 'subscribes'

    id = db.Column(db.Integer,primary_key = True)
    email= db.Column(db.String(255))
    name = db.Column(db.String(255)) 

    def __repr__(self):
        return f'User {self.email}'

    def save_subscribe(self):
       db.session.add(self)
       db.session.commit()

    @classmethod
    def get_subscribe(id):
       subscribe = Subscribe.query.all()
       return subscribe

    
