import db_utils
from flaskapp import app
from flask_script import Manager, Server

manager = Manager(app)
manager.add_command("runserver", Server(host="0.0.0.0", port=8000))

@manager.command
def rebuild_database():
    db_utils.recreate_db()
    db_utils.seed_data()

if __name__ == '__main__':
    manager.run()

