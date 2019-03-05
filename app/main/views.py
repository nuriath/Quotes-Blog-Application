from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import PostForm,UpdateProfile,CommentForm,SubscribeForm
from ..models import  User,Post,Comment,Subscribe
from flask_login import login_required,current_user
from .. import db,photos
from ..request import get_quote

@main.route('/')
def index():
    """ View root page function that returns index page """

    title = 'Home- Quotes Blog'
  
    all_posts = Post.query.all()
    quote=get_quote()
    return render_template('index.html', title = title, all_posts= all_posts, quote= quote)

def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user)

@main.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    post_form = PostForm()
    
    if post_form.validate_on_submit():
        
        post = post_form.post.data
        # user_id = post_form.user_id.data
        new_post = Post(post=post,user_id=current_user.id)
        new_post.save_post() 
    
        return redirect(url_for('main.index'))

    return render_template('new_post.html', post_form=post_form)

@main.route('/comment/new/<int:id>', methods=['GET', 'POST'])
@login_required
def comment(id):
    comment_form = CommentForm()
    
    post= Post.query.filter_by(id=id).first()
    if comment_form.validate_on_submit():
        comment = comment_form.comment.data
        # user_id = comment_form.user_id.data
        new_comment = Comment(comment=comment, post_id  = id, user_id=current_user.id)
        new_comment.save_comment()
        return redirect(url_for('main.index'))

    return render_template('comment.html',comment_form=comment_form, post= post)

@main.route('/subscribe',methods=["GET","POST"])
def subscribe():
    form=SubscribeForm()

    if form.validate_on_submit():
        email = form.email.data
        subscriber = Subscribe(email=form.email.data)
        db.session.add(subscriber)
        db.session.commit()

        mail_message=("Welcome to my blog","email/welcome_user",subscriber.email,subscriber)
        return redirect(url_for('main.index'))
        title = 'Subscribe'
    return render_template('subscribe.html',form=form)

@main.route('/delblog/<id>')
def delblog(id):
    
    blog = Blog.query.filter_by(id = id).first()
    db.session.delete(blog)
    db.session.commit()
    print(blog)
    title = 'delete blogs'
    return render_template('index.html',title = title, blog = blog)

