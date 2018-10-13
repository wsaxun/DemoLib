from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from common.conf import get_db_uri

Base = declarative_base()
metadata = Base.metadata

DB_URI = get_db_uri().get('DB_URI')


class StorageBase(object):
    def insert(self, values):
        for k, v in values.items():
            setattr(self, k, v)

        session = get_session()
        session.add(self)
        session.commit()

    def delete(self, item):
        pass

    def update(self, item, values):
        for k, v in values.items():
            setattr(self, k, v)

        # session = get_session()

    def query(self, item):
        pass


def get_engine():
    engine = create_engine(DB_URI)
    return engine


def get_session():
    engine = create_engine(DB_URI)
    session = sessionmaker(bind=engine)

    return session()
