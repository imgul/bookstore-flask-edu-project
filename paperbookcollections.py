# paperbookcollections.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookstore.db'
    
    db.init_app(app)

    # Import blueprints
    from .views import main_blueprint
    app.register_blueprint(main_blueprint)

    return app
