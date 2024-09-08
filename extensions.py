# in this file initiate global variables
from flask_sqlalchemy import SQLAlchemy

from psycopg2 import connect

from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
login = LoginManager()
mail = Mail()
admin = Admin()
bcrypt = Bcrypt()