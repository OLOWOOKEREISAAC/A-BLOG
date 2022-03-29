from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import current_user, login_required, login_user, logout_user
from app.users.utils import send_reset_mail
from app.users.forms import (Registration_form, Login_form, profile_editform,
                             reset_passwordform, reset_requestform )
from app.models import User
from app import db, bcrypt, app
import os
from PIL import Image
import secrets

users = Blueprint('users', __name__)




    

@users.route('/reset_password', methods =['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = reset_requestform()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_mail(use=user)
        flash('An Email with the reset link has been sent to your Email Please follow its instructions to change your password')
        return redirect(url_for('main.index'))
    return render_template('users/reset_request.html', form=form)


@users.route('/reset_password/<token>', methods = ['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_Rtoken(token)
    if user is None:
        flash('This link is expired')
        return redirect(url_for('reset_request'))
    form = reset_passwordform()
    if form.validate_on_submit():
        pw_hash = bcrypt.generate_password_hash(form.password1.data).decode('utf-8')
        user.password = pw_hash
        db.session.commit()
        flash('successful You can now login in ')
        return redirect(url_for('users.login'))
    return render_template('users/reset_password.html', form = form )




@users.route('/editprofile' ,  methods = ['GET', 'POST'])
def editprofile():
    form= profile_editform()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.location = form.location.data
        current_user.About_me = form.About_me.data
        db.session.commit()
        if form.profilepic.data:
            current_user.profilepic = form.profilepic.data
            hex = secrets.token_hex(8) 
            _, f_ext = os.path.split(current_user.profilepic.filename)
            pic_name = hex + f_ext
            path = os.path.join(app.root_path, 'static/pics', pic_name)
            output = (125, 125)
            I = Image.open(form.profilepic.data)
            I.thumbnail(output)
            I.save(path)
            current_user.profilepic = pic_name
            db.session.commit()
        return redirect(url_for('users.account'))
    form.name.data= current_user.name
    form.email.data= current_user.email
    form.location.data = current_user.location
    form.About_me.data = current_user.About_me
    return render_template('users/editprofile.html', form =form)

@users.route('/Account', methods = ['GET'])
@login_required
def account():
    profile_pics = url_for('static', filename='pics/' + current_user.profilepic )
    return render_template('users/account.html', profile_pics=profile_pics)





@users.route('/Login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    form = Login_form()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data ):
            login_user(user, form.Remember.data)
            flash('Login successful', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password', 'error')   
    return render_template('users/login.html', form=form)

@users.route('/Logout')
@login_required
def logout():
    logout_user()
    flash('You are now logged out', 'warning')
    return redirect(url_for('main.index'))


@users.route('/Register', methods = ['GET', 'POST'])
def Register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = Registration_form()
    if form.validate_on_submit():
        pw_harsh = bcrypt.generate_password_hash(form.password1.data).decode('utf-8')
        user = User(name = form.name.data, email = form.email.data, password = pw_harsh)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/registration.html', form=form)
