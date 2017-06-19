# -*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email,Regexp,EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('keep me logged in')
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email(),Length(1,64)])
    username=StringField('Username',validators=[
        DataRequired(),Length(1,64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Username must have only letters,number,sdots or')
    ])
    password = PasswordField('Password',validators=[
        DataRequired(),EqualTo('password2',message='must equal')])
    password2 = PasswordField('确认密码',validators=[DataRequired()])
    submit=SubmitField('注册')