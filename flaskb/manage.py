import os
from flask_script import Shell,Manager
from flask_migrate import Migrate,MigrateCommand
from app import creat_app,db
from app.models import User,Role,Post

app = creat_app(os.environ.get('FLASK_CONFIG') or 'default')
manageer = Manager(app)
migrate = Migrate(app,db)

def make_shell_context():
    return dict(app=app,db=db,User = User,Role = Role,Post=Post)

manageer.add_command('shell',Shell(make_context=make_shell_context))
manageer.add_command('db',MigrateCommand)

if __name__=='__main__':
    manageer.run()