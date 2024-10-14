import os
import logging
from flask import Flask
from database import db, run_migrations

def create_app():
    app = Flask(__name__, static_folder='static')

    # Set Flask secret key
    app.config['SECRET_KEY'] = 'supersecretflaskskey'  # TODO: Update with a secure key

    # Initialize database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
    db.init_app(app)

    # Run migrations
    from database import run_migrations
    run_migrations(app)

    return app