from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from alayatodo import app, db
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(120), unique=True)

    def __init__(self, username=None, password=None):
        self.username = username
        sel.password = password

    def __repr__(self):
        return '<User %r>' % (self.username)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), ForeignKey('users.id'))
    description = Column(String(120), unique=True)
    #complete = Column(Boolean)

    def __init__(self, user_id=None, description=None): #, complete=None
        self.user_id = user_id
        self.description = description
        #self.complete = complete

    @property
    def serialize(self):
        return {'id' : self.id,
                'user_id' : self.user_id,
                'description' : self.description }

    def __repr__(self):
        return '<Todo %r>' % (self.user_id)
