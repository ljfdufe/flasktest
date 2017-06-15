import os
from flask import Flask, render_template, session, url_for, redirect, flash
from flask_script import Manager, Shell
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
from flask_mail import Mail

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardguess'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['MAIL_SERVER'] = 'pop.126.com'
# app.config['MAIL_PORT']= 587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']=os.environ.get('MAIL_USERNAME')
app.config['MAIL_USER_PASSWORD']=os.environ.get('MAIL_PASSWORD')
manager = Manager(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
mail = Mail(app)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command('shell', Shell(make_context=make_shell_context))
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)


class NameForm(FlaskForm):
    name = StringField('what is your name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')
    # backref 作用应该是可以时插入数据时候方便，直接用User（username，role=什么role）能生产role_id


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=user)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        # return redirect(url_for('user'))   #为什么这里没重定向，反而没出现书上说的问题呢,但刷新就不行了
    return render_template('index.html', form=form,
                           name=session.get('name'),
                           known=session.get('known', False))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    manager.run()
