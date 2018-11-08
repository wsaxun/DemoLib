from sqlalchemy import Column, Integer, String, DateTime, text
from sqlalchemy.sql import func
from datetime import datetime
from common.storage.common import Base, StorageBase


class Policy(Base, StorageBase):
    __tablename__ = 'demolib_policy'

    # created_at = Column(DateTime, server_default=text("now()"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # created_at = Column(DateTime, default=datetime.now)

    now_time = Column(DateTime)
    policy_id = Column(Integer, primary_key=True)
    tenant_id = Column(String)


if __name__ == '__main__':
    from common.storage.common import create_table

    create_table()
