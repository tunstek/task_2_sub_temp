from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite://', convert_unicode=True) # testing db


#engine.execute("DROP TABLE users")

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import os, sys
    sys.path.insert(0, os.path.abspath(".."))
    import test_models
    Base.metadata.create_all(bind=engine)

def drop_all():
    for tbl in reversed(Base.metadata.sorted_tables):
        engine.execute(tbl.delete())
