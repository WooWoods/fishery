import os
import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

from app import create_app, db
from app.models import Fishes
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app,db=db,Fishes=Fishes)

manager.add_command("Shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()