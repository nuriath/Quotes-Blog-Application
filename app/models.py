from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class Post:

    all_posts = []

    def __init__(self,id,author,post):
        self.id =id
        self.author = author
        self.post = post
     
        
    def save_posts(self):
       Post.all_posts.append(self)


    @classmethod
    def clear_posts(cls):
       Post.all_posts.clear()

    @classmethod
    def get_posts(cls,id):

        response = []

        for Post in cls.all_posts:
            if Post.user_id == id:
                response.append(post)

        return response

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    post = db.relationship('Post',backref = 'user',lazy="dynamic")
    comment = db.relationship('Comment',backref = 'user',lazy="dynamic")
    profile_pic_path = db.Column(db.String(255))
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

    def save_commet(self):
        db.session.add(self)
        db.session.commit()

    def delete_comments(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(id):
        comments = Comment.query.all()
        return comments

    

class Subscribe(db.Model):
    __tablename__= 'subscribe'

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

    
