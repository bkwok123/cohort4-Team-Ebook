import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from db import db
from resources.book import Book, BookList

# Initiate Flask obj
app = Flask(__name__)

app.config['DEBUG'] = True

# https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
# In memory database only: 'sqlite:///memory'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///ebook.db')
# Turn off Flask-SQLAlchemy modifications tracking, it will use SQLAlchemy modifications tracking instead
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# https://flask.palletsprojects.com/en/1.1.x/config/
# A secret key that will be used for securely signing the session cookie
# Must have secret key before using session
app.secret_key = os.urandom(16)

# Initiate Flask-RESTful API obj
api = Api(app)

# https://flask.palletsprojects.com/en/1.1.x/quickstart/
# Add api endpoint/resource
api.add_resource(Book, '/book/<string:book_title>')
api.add_resource(BookList, '/books')

if __name__ == '__main__':
    # https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/
    # Create the database object once and configure the application later to support it
    # flask.Flask.app_context() has to exist before methods like create_all() and drop_all() will work
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000)
