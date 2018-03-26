from sqlalchemy import Column, Integer, String
import test_db

class User(test_db.Base):
    __tablename__ = 'users'
    email = Column(String(120), primary_key=True)
    password = Column(String(120), unique=False)


    def __init__(self, email=None, password=None,):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.email)
