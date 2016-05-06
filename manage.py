import db_utils
from flaskapp import app
from flask_script import Manager, Server

manager = Manager(app)
manager.add_command("runserver", Server(port=8000))

import logging.config

# load the logging configuration
logging.config.fileConfig('logging.ini', disable_existing_loggers=True)

@manager.command
def rebuild_database():
    db_utils.recreate_db()
    #db_utils.seed_data()

if __name__ == '__main__':
    manager.run()

