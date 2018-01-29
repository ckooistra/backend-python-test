from flask import Flask, g
import sqlite3
from alayatodo.database import db_session
from flask_sqlalchemy import SQLAlchemy

# configuration
DATABASE = '/tmp/alayatodo.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+'/tmp/alayatodo.db'
db = SQLAlchemy(app)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

import alayatodo.views
