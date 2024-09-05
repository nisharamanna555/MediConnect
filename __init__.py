from dotenv import load_dotenv
from flask import Flask
import os
from flask_socketio import SocketIO

from .extensions import db, login, mail, admin, bcrypt

socketio = SocketIO()
def create_app():
    # initialize instance of app
    app = Flask(__name__)
    socketio.init_app(app, cors_allowed_origins="*")

    # configure Flask app to serve static files
    app.config['STATIC_FOLDER'] = 'static'

    # configure database
    load_dotenv()
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    # app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'uploads'

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    
    app.config['WTF_CSRF_ENABLED'] = False
    
    db.init_app(app)
    login.init_app(app)
    # Initialize the mail services for contacting users via emails
    mail.init_app(app)
    admin.init_app(app)
    bcrypt.init_app(app)


    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "db_creds.json"
    
    from .routes import main
    app.register_blueprint(main)
    
    return app
