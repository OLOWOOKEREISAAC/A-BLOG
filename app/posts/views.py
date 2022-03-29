from flask import Blueprint, render_template, url_for, redirect, flash, request, abort
from app.models import Post, User
from flask_login import current_user
from app.posts.forms import blogpost_form
from app import db





posts = Blueprint('posts', __name__)


@posts.route('/post/<username>', methods =['GET'])
def users_posts(username):
    page= request.args.get('page', 1, type=int)
    user = User.query.filter_by(name =username).first_or_404()
    post = Post.query.filter_by( user =user ).order_by(Post.posted.desc()).paginate(page=page, per_page=4)
    return render_template('posts/users_post.html', post =post, user =user  )


@posts.route('/post/int:<post_id>/delete', methods= ['GET', 'POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted', 'info')
    return redirect(url_for('main.index'))




@posts.route('/post/int:<post_id>/update', methods= ['GET', 'POST'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user != current_user:
        abort(403)
    form=blogpost_form()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data  
        db.session.commit()
        flash('Post updated')
        return redirect(url_for('posts.post', post_id=post.id))
    form.title.data= post.title
    form.content.data = post.content     
    return render_template('posts/newpost.html', form= form, title = 'update post')

@posts.route('/post/int:<post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/post.html', post = post)


@posts.route('/newpost', methods = ['GET', 'POST'])
def newpost():
    form=blogpost_form()
    if form.validate_on_submit():
        p = Post(title = form.title.data, content = form.content.data, user = current_user)
        db.session.add(p)
        db.session.commit()
        flash('Post created')
        return redirect(url_for('main.index'))
    return render_template('posts/newpost.html', form=form)