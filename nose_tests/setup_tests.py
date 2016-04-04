import db_utils
from flaskapp import app
from sqlalchemy.exc import SQLAlchemyError
from flaskapp import db


class SetupTests(object):
    def __init__(self):
        self.master_test_setup()
        self.app = app.test_client()

    def _create_temp_test_db(self):
        try:
            db.reflect()
            db.drop_all()
        except SQLAlchemyError:
            pass

        db.create_all()

        db.session.commit()
        db.session.flush()

    def master_test_setup(self):
        self._create_temp_test_db()
        #db_utils.seed_data()

        db.session.commit()

    def master_test_teardown(self):
        # This is necessary to commit any pending transactions, which will make Postgres lock on DROP table queries
        db.session.commit()

        db.drop_all()
