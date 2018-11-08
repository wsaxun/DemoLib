from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from redis import ConnectionPool, StrictRedis

from common.conf import get_db_uri, get_redis_uri, get_redis_pool_num

Base = declarative_base()
metadata = Base.metadata

DB_URI = get_db_uri().get('DB_URI')


def singleton(cls):
    instance = {}

    @wraps(cls)
    def inner(*args, **kwargs):
        if id(cls) not in instance:
            instance[id(cls)] = cls(*args, **kwargs)
        return instance[id(cls)]

    return inner


class StorageBase(object):
    def insert(self, values):
        for k, v in values.items():
            setattr(self, k, v)
        setattr(self, 'session', get_session())
        self.session.add(self)
        self._commit()

    def delete(self, query_item):
        self._query(query_item).delete()
        self._commit()

    def update(self, query_item, values):
        self._query(query_item).update(values)
        self._commit()

    def query(self, query_item):
        return self._query(query_item)

    @classmethod
    def _query(cls, query_item):
        session = get_session()
        setattr(cls, 'session', session)
        items = session.query(cls).filter_by(**query_item)
        return items

    def _commit(self):
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
        finally:
            self.session.close()


@singleton
class RedisClient:
    def __init__(self):
        self.redis = StrictRedis(connection_pool=self._pool())

    @staticmethod
    def _pool():
        max_connections = get_redis_pool_num()
        pool = ConnectionPool.from_url(get_redis_uri(),
                                       max_connections=max_connections)
        return pool

    def __getattr__(self, api):
        api = getattr(self.redis, api, None)
        if not api:
            raise AttributeError('redis have not this method')
        return api


def get_engine():
    engine = create_engine(DB_URI)
    return engine


def get_session():
    engine = get_engine()
    session = sessionmaker(bind=engine)
    return session()


def create_table():
    engine = get_engine()
    metadata.create_all(engine)
