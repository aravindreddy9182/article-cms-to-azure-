"""
The flask application package.
"""
import logging
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
Session(app)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

# Import views AFTER creating app
import FlaskWebProject.views

# 🔥 AUTO CREATE TABLES + ADMIN USER
from FlaskWebProject.models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()   # create tables if not exist

    if not User.query.filter_by(username="admin").first():
        user = User(username="admin")
        user.password_hash = generate_password_hash("pass")
        db.session.add(user)
        db.session.commit()
        print("✅ Admin user created (admin/pass)")
