# -*- coding:utf-8 -*-
from flask import render_template,redirect,url_for,flash,request
from flask_login import login_user,login_required,logout_user,current_user
#current_user  就是定义的user 模型
from . import auth
from .forms import LoginForm,RegistrationForm
from ..models import User
from .. import db
from ..email import send_email


@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user=user,remember=form.remember_me.data)
            return redirect((request.args.get('next')) or url_for('main.index'))
        flash('invalid username or password')
    return render_template('auth/login.html',form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('you have been logged out')
    return redirect(url_for('main.index'))

@auth.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        token = user.generate_confirmation_token()
        send_email(to=form.email.data,subject='confirm yout count',
                   template='auth/email/confirm',user=user,token=token)
        flash('发送了一封确认邮件')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html',form=form)

@auth.route('/confirm<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirmed(token):
        flash('you have confirmed')
    else:
        flash('the confirmation link is invalid')
    return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
            and request.endpoint \
            and request.endpoint[:5] != 'auth.'\
            and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(to=current_user.email, subject='confirm yout count',
               template='auth/email/confirm', user=current_user, token=token)
    flash('发送了一封确认邮件')
    return redirect(url_for('main.index'))