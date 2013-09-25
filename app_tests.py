import os
import app
import unittest
from app import db


class VinneratorTestCase(unittest.TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite://"

    def create_app(self):
        print "Initializing the database"
        app.init_db()

    def setUp(self):
        self.app = app.app.test_client()  # this is really confusing, but works???
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_empty_db(self):
        rv = self.app.get('/show_entries')
        assert 'No entries here so far' in rv.data

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
            ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('admin', 'password')
        #assert 'You were logged in' in rv.data
        assert 'log out' in rv.data
        rv = self.logout()
        assert 'log in' in rv.data
        rv = self.login('adminx', 'default')
        assert 'Invalid username' in rv.data
        rv = self.login('admin', 'defaultx')
        assert 'Invalid password' in rv.data

    def test_messages(self):
        #self.create_app()
        self.login('admin', 'password')
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert 'No entries here so far' not in rv.data
        assert '&lt;Hello&gt;' in rv.data
        assert '<strong>HTML</strong> allowed here' in rv.data

if __name__ == '__main__':
    unittest.main()









