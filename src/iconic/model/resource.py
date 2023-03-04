from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Resource(Base):
    __tablename__ = 'resource'
    resource_name = Column(String, primary_key=True)
    resource_url = Column(String)
    resource_password = Column(String)
