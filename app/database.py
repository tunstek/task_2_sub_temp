from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql://root:root@db', convert_unicode=True, pool_recycle=3600) # Docker-compose seperate db

engine.execute("CREATE DATABASE IF NOT EXISTS task_2_db")
engine.execute("USE task_2_db")

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
    import models
    Base.metadata.create_all(bind=engine)

def drop_all():
    for tbl in reversed(Base.metadata.sorted_tables):
        engine.execute(tbl.delete())
