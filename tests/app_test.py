
from flask import Flask
import pytest
import unittest
from sqlalchemy.exc import IntegrityError
from passlib.hash import pbkdf2_sha256

import os, sys
sys.path.insert(0, os.path.abspath(".."))
import test_db as db
from test_models import User


class TestCases(unittest.TestCase):

    @classmethod
    def setup_class(self):
        # Creates a new database for the unit test to use
        self.app = Flask(__name__)
        db.init_db()

        self.test_email = "test@test.com"
        self.test_psw = "test_pass"
        self.test_hashed_psw = pbkdf2_sha256.encrypt(self.test_psw, rounds=200000, salt_size=16)

        with self.app.app_context():
            self.populate_db() # add test data.

    @classmethod
    def teardown_class(self):
        # Ensures that the database is emptied for next unit test
        db.drop_all()

    @classmethod
    def populate_db(self):
        db.drop_all() # teardown_class doesn't seem to get called after test failure???
        # add user to DB
        usr = User(email=self.test_email, password=self.test_hashed_psw)
        db.db_session.add(usr)
        db.db_session.commit()






    ###########################################
    ############### TEST CASES ################
    ###########################################
    @classmethod
    def test_user_creation(self):
        user = db.db_session.query(User).filter_by(email=self.test_email).first()
        self.assertTrue(user)

    @classmethod
    def test_duplicate_user(self):
        usr = User(email=self.test_email, password=self.test_hashed_psw)
        db.db_session.add(usr)
        try:
            # commit the user
            db.db_session.commit()
        except IntegrityError:
            pass
        except Exception as e:
            self.fail("Unexpected exception raised:" + str(e))
        else:
            self.fail("IntegrityError not raised")
        db.db_session.rollback()

    @classmethod
    def test_hash_validation(self):
        self.user = db.db_session.query(User).filter_by(email=self.test_email).first()
        self.assertTrue(pbkdf2_sha256.verify(self.test_psw, self.user.password))
        self.assertFalse(pbkdf2_sha256.verify("wrong_password", self.user.password))





if __name__ == '__main__':
    unittest.main()
