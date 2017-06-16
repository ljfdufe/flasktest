from flask import render_template,session
from .forms import NameForm
from . import main
from ..models import User,Role
from .. import db

@main.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@main.route('/', methods=['GET', 'POST'])
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