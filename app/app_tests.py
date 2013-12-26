from flask.ext.testing import TestCase
from app import app, db


class MyTest(TestCase):

    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/cap_test_db"
    TESTING = True
    DEBUG = True

    def create_app(self):
        return app

    def setUp(self):

        db.create_all()

    def tearDown(self):

        db.session.remove()
        db.drop_all()





