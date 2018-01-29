from flask import Flask
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
def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


#@app.before_request
#def before_request():
#    g.db = connect_db()


#@app.teardown_request
#def teardown_request(exception):
#    db = getattr(g, 'db', None)
#    if db is not None:
#        db.close()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

import alayatodo.views
