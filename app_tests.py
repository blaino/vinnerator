import os
import unittest

os.environ["DATABASE_URL"] = "sqlite://"

import app
from app import db, views

#app.app.config['TESTING'] = True
app.app.config['WTF_CSRF_ENABLED'] = False
#app.app.config['LOGIN_DISABLED'] = True


class MyappTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def register(self, email, password):
        return self.app.post('/register', data=dict(email=email,
                                                    password=password,
                                                    password_confirm=password
                                                    ), follow_redirects=True)

    # def login(self, email, password):
    #     return self.app.post('/login', data=dict(email=email,
    #                                              password=password
    #                                              ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def sample_output(self):
        return dict(title='default',
                    cash_on_cash='10.0',
                    target_ltv='80.0',
                    interest='6.0',
                    amort='30.0',
                    mezz_debt='0.0',
                    transfer_cost='2.0',
                    transfer_buyer_share='50.0',
                    recordation_cost='5.0',
                    recordation_buyer_share='50.0',
                    finance='1.0',
                    apprec_depr='0.0',
                    holding_period='5.0'
                    )

    def add(self):
        return self.app.post('/add', data=self.sample_output(), follow_redirects=True)

    def delete(self, index):
        url = '/delete/' + str(index)
        return self.app.get(url, follow_redirects=True)

    def test_basic_page(self):
        rv = self.app.get('/basic', follow_redirects=True)
        assert 'This is the basic calculation' in rv.data

    def test_basic_calc(self):
        resp = self.app.post('/basic_calc', data=self.sample_output(), follow_redirects=True)
        assert 'Cap Rate: 7.756' in resp.data

    def test_register_logout(self):
        rv = self.register('blue@blue.com', 'password')
        assert 'Mezzanine' in rv.data
        rv = self.logout()
        assert 'Click here to find out' in rv.data

    def test_add(self):
        self.register('blue@blue.com', 'password')
        resp = self.add()
        assert '7.80%' in resp.data

    def test_to_boolean(self):
        yesno = 'Y'
        assert views.to_boolean(yesno) is True
        yesno = 'N'
        assert views.to_boolean(yesno) is False
        yesno = 'Yes'
        assert views.to_boolean(yesno) is True
        yesno = 'No'
        assert views.to_boolean(yesno) is False
        yesno = 'y'
        assert views.to_boolean(yesno) is True
        yesno = 'n'
        assert views.to_boolean(yesno) is False
        yesno = 'yes'
        assert views.to_boolean(yesno) is True
        yesno = 'no'
        assert views.to_boolean(yesno) is False
        yesno = 'garbage'
        assert views.to_boolean(yesno) is False

    def add3(self):
        self.register('blue@blue.com', 'password')
        self.add()
        self.add()
        return self.add()

    def test_add_3_scenarios_with_same_name(self):
        rv = self.add3()
        assert 'default&lt;2&gt;' in rv.data  # default<2>

    def test_add_3_then_delete_second(self):
        rv = self.add3()
        rv = self.delete('2')
        assert 'default' in rv.data
        assert 'default&lt;1&gt;' not in rv.data  # default<1> shoudln't be there

    def test_add_3_then_delete_last(self):
        rv = self.add3()
        rv = self.delete('3')
        assert 'default' in rv.data
        assert 'default&lt;2&gt;' not in rv.data  # default<2> shoudln't be there

    def test_add_3_then_delete_first(self):
        rv = self.add3()
        rv = self.delete('1')
        assert 'default' in rv.data
        assert '<option value="1">default</option>' not in rv.data  # default shoudln't be there
        # And neither should default<1> when mapped to value=0
        assert '<option value="0">default&lt;1&gt;</option>' not in rv.data

    def test_delete_default(self):
        self.register('blue@blue.com', 'password')
        rv = self.delete('None')
        assert '<option value="None" selected>default</option>' in rv.data

if __name__ == '__main__':
    unittest.main()
