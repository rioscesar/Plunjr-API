from flaskapp import app
from flask_script import Manager, Server

manager = Manager(app)
manager.add_command("runserver", Server(host="0.0.0.0", port=8000))

if __name__ == '__main__':
    manager.run()

