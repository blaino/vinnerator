from flask import Flask
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy

# Initialization
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
mail = Mail(app)
app.extensions['mail'] = mail

from app import models, views
