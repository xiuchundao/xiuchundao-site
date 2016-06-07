#!/usr/bin/env python
from flask_script import Manager
from flask_migrate import Migrate, init, upgrade, migrate

from app import create_app, db

app = create_app('default')
manager = Manager(app)
x_migrate = Migrate(app, db)


@manager.command
def create_db():
    """Create a database."""
    init()
    upgrade_db()


@manager.command
def upgrade_db():
    migrate()
    upgrade()

if __name__ == '__main__':
    manager.run()
