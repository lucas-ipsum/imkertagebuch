# Applikation wird initialisiert
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '03bb4af5de86889dfb14b261d7094a93'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:cCxKqZxfhr18YACY@localhost:5432/imkertagebuch'


engine = create_engine('postgresql://postgres:cCxKqZxfhr18YACY@localhost:5432/imkertagebuch')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from imkertagebuch import routes
