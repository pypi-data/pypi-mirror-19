#!/usr/bin/env python

from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand

from ara import app
from ara.models import db

manager = Manager(app)
manager.add_command('db', MigrateCommand)
migrate = Migrate(app, db, directory=app.config['DB_MIGRATIONS'])


@manager.command
def createall():
    db.create_all()


@manager.command
def dropall():
    """ Drops all database tables """

    if prompt_bool("Are you sure ? You will lose all your data !"):
        db.drop_all()


def main():
    manager.run()


if __name__ == '__main__':
    main()
