from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_cors import CORS, cross_origin
import os

load_dotenv()
db = SQLAlchemy()
mail = Mail()
def create_app():
    app = Flask(__name__)
    # database config
    app.config['SQLALCHEMY_DATABASE_URI'] =f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DATABASE')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    #mail config
    app.config['MAIL_PORT']=os.getenv('MAIL_PORT')
    app.config['MAIL_DEBUG']=False

    #cors config
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    db.init_app(app)
    mail.init_app(app)

    with app.app_context():
        db.create_all()

    # Importing routes
    from routes import user_routes
    app.register_blueprint(user_routes)

    return app