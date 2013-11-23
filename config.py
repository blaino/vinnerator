import os

# For local use: export DATABASE_URL="postgresql://localhost/vinnerator_db"
# (That's what heroku sets)
SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
USERNAME = "admin"
PASSWORD = "password"
TESTING = False
DEBUG = True
SECRET_KEY = ')\xd4\xa0\xbf@\xce\x81tol\xdbrae\xd0\xc6\x0b#\xf1\xc5\x11@\xdd\xcc'
SECURITY_LOGIN_URL = '/login'
SECURITY_POST_LOGIN_VIEW = '/show_scenarios'
SECURITY_POST_LOGOUT_VIEW = '/'
SECURITY_REGISTERABLE = True
SECURITY_POST_REGISTER_VIEW = '/show_scenarios'
SECURITY_SEND_REGISTER_EMAIL = False
CSRF_ENABLED = True
