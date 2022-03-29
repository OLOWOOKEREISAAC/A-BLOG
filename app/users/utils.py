from app.models import User
from flask_mail import Message
from flask import url_for
from app import mail




def send_reset_mail(use):
    token = User.generate_Rtoken(use)
    msg = Message('Password', recipients=[use.email], sender='Flask Practice' )
    
    msg.body = f''' Dear{use.name}: 
Click this the link below to change your password 
{url_for('reset_password', token = token, _external =True)}

If you did not make this request please contact us via whatsusers on
08138399882
'''
    mail.send(msg)